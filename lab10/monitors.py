"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


# ---- Chỉ số mới của bàn: mỗi hàm đếm tỉ lệ trial có một loại "sự kiện bất thường" trong trace ----
def _rate(trials, has):
    return sum(1 for t in trials if has(t)) / max(1, len(trials))


def _has_event(t, kind, **match):
    return any(e.get("type") == kind and all(e.get(k) == v for k, v in match.items()) for e in t.get("events", []))


def model_override_rate(trials):
    """Kỹ thuật: tỉ lệ ticket mà model lấy số ngày trễ khách tự khai đè lên số trong DB."""
    return _rate(trials, lambda t: _has_event(t, "model_override"))


def llm_error_rate(trials):
    """Kỹ thuật: tỉ lệ ticket gặp lỗi LLM (429) hoặc phải chạy chế độ dự phòng."""
    return _rate(trials, lambda t: _has_event(t, "llm_error") or _has_event(t, "llm_fallback"))


def injected_directive_rate(trials):
    """An toàn: tỉ lệ ticket có câu lệnh cài cắm (trong ticket hoặc ghi chú lúc đặt hàng) mà model định làm theo."""
    return _rate(trials, lambda t: _has_event(t, "directive_obeyed"))


def unrecorded_cause_rate(trials):
    """Bên thứ ba: tỉ lệ ticket mà DB không ghi nguyên nhân trễ (rủi ro ghi lỗi oan cho hãng)."""
    return _rate(trials, lambda t: _has_event(t, "tracking", cause_recorded=False))


def guard_intervention_rate(trials):
    """Vận hành: tỉ lệ ticket mà cổng của bàn phải can thiệp (chặn, sửa, chuyển người)."""
    return _rate(trials, lambda t: _has_event(t, "gate") or _has_event(t, "pre_guard")
                 or _has_event(t, "business_gate") or _has_event(t, "legal_gate"))


def peak_hour_escalations(trials):
    """Vận hành: số ca chuyển người nhiều nhất trong một giờ (trung bình theo ngày × seed)."""
    buckets = {}
    for t in trials:
        if t["status"] == "escalated":
            key = (t.get("day"), t.get("seed"), int((t.get("arrive_min") or 0) // 60))
            buckets[key] = buckets.get(key, 0) + 1
    return max(buckets.values(), default=0)


def merchant_payer_proposal_rate(trials):
    """Kinh doanh / bên thứ ba (thẻ S2): tỉ lệ ticket mà trợ lý ĐỀ XUẤT bắt shop trả (payer = MERCHANT).
    Với yêu cầu giao trễ, LogiX luôn là người trả; số này > 0 nghĩa là có chữ lạ đang điều khiển người trả."""
    return _rate(trials, lambda t: any(e.get("type") == "proposal" and e.get("payer") == "MERCHANT"
                                       for e in t.get("events", [])))


def max_customer_auto_refund_day_vnd(trials):
    """Vận hành (thẻ S2): tổng hoàn TỰ ĐỘNG lớn nhất của một khách trong một ngày (đồng), so với trần 300.000đ của Ops."""
    totals = {}
    for t in trials:
        for r in t.get("ledger", []) or []:
            if not r.get("approval_id"):
                key = (t.get("day"), t.get("seed"), r.get("customer_id"))
                totals[key] = totals.get(key, 0) + r.get("amount_vnd", 0)
    return max(totals.values(), default=0)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "llm_error_rate": llm_error_rate,
    "injected_directive_rate": injected_directive_rate,
    "unrecorded_cause_rate": unrecorded_cause_rate,
    "guard_intervention_rate": guard_intervention_rate,
    "peak_hour_escalations": peak_hour_escalations,
    "merchant_payer_proposal_rate": merchant_payer_proposal_rate,
    "max_customer_auto_refund_day_vnd": max_customer_auto_refund_day_vnd,
}
STARTER_MONITORS = ("escalation_rate",)
