"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ---------------------------------------------------------------------------
# Hàm phụ: tính lại "sự thật" từ hệ thống (DB), KHÔNG tin chữ khách viết
# ---------------------------------------------------------------------------
def _facts(ctx, order_id):
    """Đơn hàng, kiện bị trễ, số ngày trễ theo DB, chính sách đang hiệu lực hôm nay."""
    order = ctx.tools.lookup_order(order_id)
    if order is None:
        return None
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    return {"order": order, "policy": policy, "parcel": parcel, "delay": delay}


# ---------------------------------------------------------------------------
# CỔNG 0 · pre_guard: ghim phiên bản chính sách theo NGÀY, không theo cờ "index_active"
# (rủi ro HAZOP: đầu vào "hết hiệu lực" — chỉ mục chính sách chưa cập nhật)
# ---------------------------------------------------------------------------
def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách nào hiệu lực hôm nay")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")

    # -----------------------------------------------------------------------
    # CỔNG 1 · issue_refund: số tiền phải khớp chính sách + dữ liệu DB
    # (chặn: model tin số ngày khách tự khai, làm theo lệnh cài trong ticket,
    #  "fail-open" khi LLM lỗi 429, hoàn trùng, dùng phê duyệt không hợp lệ)
    # -----------------------------------------------------------------------
    if tool == "issue_refund":
        f = _facts(ctx, action.get("order_id"))
        if f is None or f["policy"] is None:
            return Verdict.escalate("không tra được đơn hoặc chính sách để kiểm số tiền")
        order, policy = f["order"], f["policy"]

        # 1a. Không hoàn trùng: đơn này đã có dòng hoàn trong sổ cái thì không hoàn nữa
        if ctx.tools.ledger_rows(order_id=order["order_id"]):
            ctx.log("duplicate_refund_blocked", order_id=order["order_id"])
            return Verdict.deny("đơn đã có khoản hoàn trong sổ cái")

        # 1b. Tính lại số tiền đúng theo DB (không dùng số ngày khách tự khai)
        expected = H.entitlement_vnd(policy, order, f["delay"], f["parcel"].get("delay_cause"))
        asked = int(action.get("amount_vnd") or 0)
        if expected <= 0:
            ctx.log("refund_not_entitled", asked=asked, db_delay=f["delay"])
            return Verdict.deny("theo dữ liệu hệ thống, đơn chưa đủ điều kiện hoàn")

        changes = {}
        if asked != expected:
            ctx.log("refund_amount_fixed", asked=asked, expected=expected)
            changes["amount_vnd"] = expected
        if action.get("payer", "LOGIX") != "LOGIX":          # trễ giao là lỗi phía giao hàng, không bắt shop trả
            changes["payer"] = "LOGIX"

        # 1c. Vượt hạn mức tự động thì phải có phê duyệt HỢP LỆ cho ĐÚNG đơn này
        if expected > policy["auto_limit_vnd"]:
            appr = None
            aid = action.get("approval_id")
            if aid:
                appr = next((a for a in ctx.tools.lookup_approvals(approval_id=aid)), None)
            approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            ok = (appr is not None
                  and appr.get("order_id") == order["order_id"]
                  and appr.get("status") == "valid"
                  and appr.get("expires_at", "") >= ctx.as_of
                  and appr.get("max_vnd", 0) >= expected
                  and (not approver or appr.get("approver_id") == approver))
            if not ok:
                ctx.log("approval_invalid", approval_id=aid)
                return Verdict.escalate("vượt hạn mức tự động, phê duyệt không hợp lệ cho đơn này")

        if changes:
            return Verdict.modify("chỉnh theo chính sách và dữ liệu hệ thống", **changes)
        return Verdict.allow()

    # -----------------------------------------------------------------------
    # CỔNG 2 · file_carrier_fault: chỉ ghi lỗi hãng khi DB có nguyên nhân thuộc lỗi hãng,
    # đúng kiện bị trễ, đúng hãng, và chưa vượt trần lỗi/ngày đã thống nhất
    # (bảo vệ bên thứ ba: hãng nhỏ, tài xế)
    # -----------------------------------------------------------------------
    if tool == "file_carrier_fault":
        f = _facts(ctx, action.get("order_id"))
        if f is None or f["policy"] is None:
            return Verdict.deny("không tra được đơn hoặc chính sách để ghi lỗi hãng")
        parcel = f["parcel"]
        if not H.carrier_at_fault(f["policy"], parcel, f["delay"]):
            ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"))
            return Verdict.deny("không có nguyên nhân lỗi hãng được ghi nhận cho kiện bị trễ")

        limit = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if limit is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= limit:
            ctx.log("carrier_strike_cap", carrier_id=parcel["carrier_id"])
            return Verdict.deny("hãng đã chạm trần lỗi tự động trong ngày, để người ghi")

        right = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                 "driver_id": parcel.get("driver_id"), "delay_days": f["delay"]}
        if any(action.get(k) != v for k, v in right.items()):
            ctx.log("carrier_fault_fixed", asked={k: action.get(k) for k in right}, fixed=right)
            return Verdict.modify("ghi lỗi đúng kiện, đúng hãng, đúng số ngày trễ theo DB", **right)
        return Verdict.allow()

    # -----------------------------------------------------------------------
    # CỔNG 3 · notify_carrier: chỉ gửi cho hãng đúng các trường chính sách cho phép
    # (không gửi chữ khách viết, tên / số điện thoại người nhận → không lộ dữ liệu cá nhân)
    # -----------------------------------------------------------------------
    if tool == "notify_carrier":
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        allowed = set((policy or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "delay_days"])
        payload = action.get("payload") or {}
        clean = {k: v for k, v in payload.items() if k in allowed}
        if clean != payload:
            ctx.log("pii_stripped", dropped=sorted(set(payload) - set(clean)))
            return Verdict.modify("chỉ gửi trường chính sách cho phép", payload=clean)
        return Verdict.allow()

    return Verdict.allow()
