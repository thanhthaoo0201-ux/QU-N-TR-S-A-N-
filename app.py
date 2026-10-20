                st.success(f"Đặt hàng thành công! Mã đơn của bạn: **{order_id}**")
                st.info("Hãy mở mục “Theo dõi đơn” để xem trạng thái và QR thanh toán.")
                st.rerun()

# =========================================================
# MOOD MATCH & QUẺ BÓI
# =========================================================
elif page == "Mood Match & Quẻ bói":
    st.subheader("💗 Mood Match — hôm nay bạn đang cảm thấy thế nào?")
    st.write("Chọn tâm trạng để nhận gợi ý món phù hợp. Đây là gợi ý vui, bạn vẫn có thể chọn bất kỳ món nào.")
    mood = st.radio("Tâm trạng của bạn", ["Cần năng lượng", "Cần tập trung", "Cần thư giãn",
                    "Muốn được vỗ về", "Muốn đổi gió", "Nóng nực", "Vui vẻ"], horizontal=False)
    if st.button("✨ Tìm món hợp mood", type="primary"):
        matches = [(n, x) for n, x in MENU.items() if mood in x["mood"]]
        if matches:
            random.shuffle(matches)
            st.session_state.mood_results = matches[:3]
    for name, item in st.session_state.get("mood_results", []):
        with st.container(border=True):
            a, b = st.columns([1, 2])
            with a:
                st.image(item["image"], use_container_width=True)
            with b:
                st.markdown(f"### {name}")
                st.write(item["desc"])
                st.markdown(f"**{money(item['price'])}**")
                if st.button(f"Chọn {name}", key=f"mood_{name}"):
                    st.session_state.selected_product = name
                    st.info("Món đã được chọn. Quay lại mục Đặt món để tuỳ chỉnh và thêm vào giỏ.")
    st.divider()
    st.subheader("🔮 Quẻ bói trà sữa hôm nay")
    st.write("Một chiếc quẻ vui để bạn lấy cảm hứng chọn món — không phải dự đoán tương lai.")
    if st.button("Rút một quẻ"):
        fortunes = [
            ("Quẻ Ngọt Ngào 🍓", "Hôm nay hãy cho bản thân một điều dễ chịu. Gợi ý: Trà sữa dâu tây."),
            ("Quẻ Bình Yên 🍵", "Chậm lại một chút, nhấp một ngụm trà và nghỉ ngơi. Gợi ý: Matcha latte."),
            ("Quẻ Bứt Phá ⚡", "Một khởi đầu nhỏ cũng đáng tự hào. Gợi ý: Americano hoặc trà chanh dây."),
            ("Quẻ May Mắn 🌈", "Thử điều mới mẻ để đổi vị ngày hôm nay. Gợi ý: Soda việt quất."),
            ("Quẻ Dịu Dàng 🌷", "Bạn xứng đáng được chiều chuộng. Gợi ý: Ô long kem cheese."),
        ]
        title, message = random.choice(fortunes)
        st.session_state.fortune = (title, message)
    if "fortune" in st.session_state:
        st.success(f"**{st.session_state.fortune[0]}**\n\n{st.session_state.fortune[1]}")

# =========================================================
# VÒNG QUAY
# =========================================================
elif page == "Vòng quay voucher":
    st.subheader("🎡 Vòng quay may mắn")
    st.write("Mỗi phiên chỉ quay một lần. Voucher chỉ là tính năng demo; quán cần xác nhận điều kiện áp dụng.")
    st.markdown("""
    <div style="font-size:56px;text-align:center;padding:20px;border-radius:20px;
    background:conic-gradient(#f7c9d4 0 72deg,#f4d9a6 72deg 144deg,#d8e9d4 144deg 216deg,
    #d7d9f8 216deg 288deg,#f0e5df 288deg 360deg);">🎁 🎉 🧋 🎟️ 🍀</div>
    """, unsafe_allow_html=True)
    if not st.session_state.spun:
        if st.button("🎯 QUAY NGAY", type="primary", use_container_width=True):
            prize = random.choice(VOUCHERS)
            st.session_state.spun = True
            st.session_state.won_voucher = prize
            st.session_state.voucher = {"name": prize["name"], "discount": "topping" if prize["name"] == "Tặng topping" else prize["discount"]}
            st.rerun()
    else:
        prize = st.session_state.get("won_voucher", {"name": "Chưa có voucher"})
        st.success(f"🎉 Bạn nhận được: **{prize['name']}**")
        st.caption("Voucher được lưu trong phiên hiện tại và sẽ mất khi phiên app khởi động lại.")
        if st.button("Quay lại đặt món"):
            st.session_state["page"] = "Đặt món"
            st.info("Chọn “Đặt món” ở thanh bên để tiếp tục.")
    if st.session_state.voucher:
        st.info(f"Voucher đang giữ: {st.session_state.voucher['name']}")

# =========================================================
# THEO DÕI ĐƠN
# =========================================================
elif page == "Theo dõi đơn":
    st.subheader("📦 Theo dõi đơn hàng")
    st.write("Nhập mã đơn được hiển thị sau khi đặt hàng.")
    default_id = st.session_state.last_order_id or ""
    lookup_id = st.text_input("Mã đơn hàng", value=default_id, placeholder="Ví dụ: MALA-261020-1234")
    if lookup_id and lookup_id in st.session_state.orders:
        order = st.session_state.orders[lookup_id]
        st.markdown(f"### Đơn {order['id']}")
        st.caption(f"Thời gian đặt: {order['created']}")
        status_steps = ["Đã tiếp nhận", "Đang pha chế", "Đang giao hàng", "Hoàn thành"]
        current = status_steps.index(order["status"]) if order["status"] in status_steps else 0
        st.progress((current + 1) / len(status_steps), text=f"Trạng thái: {order['status']}")
        st.write("**Các bước đơn hàng**")
        for i, step in enumerate(status_steps):
            st.write(("🟢" if i <= current else "⚪") + " " + step)
        st.dataframe(pd.DataFrame(order["items"])[["Tên món", "Size", "Đường", "Đá", "Topping", "Ghi chú", "Số lượng", "Thành tiền"]],
                     use_container_width=True, hide_index=True)
        st.metric("Tổng thanh toán", money(order["total"]))
        with st.expander("Thông tin giao hàng"):
            st.write(f"Khách hàng: {order['customer']}")
            st.write(f"Số điện thoại: {order['phone']}")
            st.write(f"Địa chỉ: {order['address']}")
        st.markdown("#### 💳 QR thanh toán")
        qr = vietqr_url(order["total"], order["id"])
        if qr:
            st.image(qr, caption=f"Quét QR và nhập nội dung chuyển khoản: {order['id']}", width=300)
            st.caption("QR được tạo từ thông tin ngân hàng do chủ quán nhập trong Cài đặt thanh toán. Hãy kiểm tra kỹ trước khi sử dụng.")
        else:
            st.warning("Chưa cấu hình ngân hàng. Vào “Cài đặt thanh toán” để nhập mã ngân hàng và số tài khoản; QR sẽ hiển thị tại đây.")
        st.caption("Trạng thái demo do khách/nhân viên cập nhật thủ công, chưa kết nối đơn vị vận chuyển.")
        with st.expander("Khu vực nhân viên: cập nhật trạng thái (demo)"):
            new_status = st.selectbox("Trạng thái mới", status_steps, index=current, key=f"status_{lookup_id}")
            if st.button("Cập nhật trạng thái", key=f"update_{lookup_id}"):
                order["status"] = new_status
                st.success("Đã cập nhật trạng thái demo.")
                st.rerun()
    elif lookup_id:
        st.info("Không tìm thấy mã đơn này trong phiên chạy hiện tại. Nếu app đã khởi động lại, dữ liệu demo có thể đã mất.")

# =========================================================
# TÍCH ĐIỂM & ĐÁNH GIÁ
# =========================================================
elif page == "Tích điểm & Đánh giá":
    st.subheader("⭐ Thành viên MAMALALA")
    st.metric("Điểm hiện có", st.session_state.points)
    st.write("Quy tắc demo: mỗi 10.000đ thanh toán được cộng 1 điểm. Khi triển khai thật, nên lưu điểm theo số điện thoại/tài khoản khách hàng.")
    st.divider()
    st.subheader("💬 Đánh giá trải nghiệm")
    completed_orders = [o for o in st.session_state.orders.values() if o["status"] == "Hoàn thành"]
    if not completed_orders:
        st.info("Bạn cần có đơn hàng ở trạng thái “Hoàn thành” để gửi đánh giá.")
    else:
        order_options = [o["id"] for o in completed_orders]
        review_order = st.selectbox("Chọn đơn hàng", order_options)
        rating = st.slider("Bạn chấm quán mấy sao?", min_value=1, max_value=5, value=5)
        review_text = st.text_area("Nhận xét", placeholder="Đồ uống, đóng gói, giao hàng...")
        if st.button("Gửi đánh giá", type="primary"):
            st.session_state.ratings.append({
                "Mã đơn": review_order, "Số sao": rating, "Nhận xét": review_text,
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Cảm ơn bạn đã đánh giá MAMALALA!")
    if st.session_state.ratings:
        st.divider()
        st.subheader("Đánh giá đã gửi")
        st.dataframe(pd.DataFrame(st.session_state.ratings), use_container_width=True, hide_index=True)

# =========================================================
# CẤU HÌNH QR
# =========================================================
elif page == "Cài đặt thanh toán":
    st.subheader("⚙️ Cài đặt QR thanh toán")
    st.warning("Chỉ nhập thông tin tài khoản nhận tiền chính thức của quán. Đừng dùng thông tin mẫu khi công khai website.")
    st.write("QR dùng dịch vụ VietQR để tạo mã chuyển khoản theo số tiền và mã đơn.")
    bank_id = st.text_input("Mã ngân hàng VietQR", value=st.session_state.get("bank_id", ""), placeholder="Ví dụ: mã ngân hàng theo VietQR")
    account_no = st.text_input("Số tài khoản", value=st.session_state.get("account_no", ""), placeholder="Số tài khoản nhận tiền")
    account_name = st.text_input("Tên chủ tài khoản", value=st.session_state.get("account_name", ""), placeholder="TÊN CHỦ TÀI KHOẢN")
    if st.button("Lưu cấu hình trong phiên này", type="primary"):
        st.session_state.bank_id = bank_id.strip()
        st.session_state.account_no = account_no.strip()
        st.session_state.account_name = account_name.strip()
        st.success("Đã lưu trong phiên chạy hiện tại.")
    st.caption("Cấu hình này chưa được lưu bền vững. Không đưa thông tin bí mật vào mã nguồn công khai.")
