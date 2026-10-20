import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import uuid
import random
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

# =========================================================
# Tiệm trà Ú Nu — Streamlit shop
# Run: streamlit run app.py
# =========================================================

st.set_page_config(
    page_title="Tiệm trà Ú Nu",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME / CSS --------------------
# Main fix: explicit dark text colors on light backgrounds.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root {
  --pink: #e9a9bd;
  --pink-dark: #b85e7d;
  --pink-light: #fff3f6;
  --cream: #fffaf8;
  --ink: #292832;
  --muted: #66616b;
  --line: #f0dce3;
  --card: #ffffff;
}
html, body, [class*="css"], .stApp {
  font-family: 'Be Vietnam Pro', sans-serif !important;
}
.stApp {
  background: linear-gradient(180deg, #fffaf9 0%, #fff5f7 100%);
  color: var(--ink) !important;
}
[data-testid="stHeader"] { background: rgba(255,250,249,.92); }
[data-testid="stSidebar"] {
  background: #fff2f5 !important;
  border-right: 1px solid #f0dce3;
}
[data-testid="stSidebar"] * {
  color: #302832 !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
  color: #302832;
}
h1, h2, h3, h4, p, label, li, .stMarkdown, [data-testid="stCaptionContainer"] {
  color: #292832;
}
h1 { letter-spacing: -1.2px; }
p, li, label, .stCaption { line-height: 1.55; }
small, [data-testid="stCaptionContainer"] { color: #68616a !important; }
div[data-testid="stMetric"] {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 15px 18px;
  box-shadow: 0 4px 18px rgba(100,50,70,.04);
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
  color: #292832 !important;
}
div[data-testid="stForm"] {
  background: #fff;
  border: 1px solid var(--line);
  padding: 18px;
  border-radius: 18px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--line) !important;
  border-radius: 18px !important;
}
.stButton > button, .stDownloadButton > button, button[kind="primary"] {
  border-radius: 13px !important;
  border: 1px solid #e5a6bb !important;
  font-weight: 700 !important;
  min-height: 43px;
  color: #292832 !important;
  background: #ffe7ef !important;
  transition: .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background: #f8d1df !important;
  border-color: #c87895 !important;
}
button[kind="primary"] {
  color: #fff !important;
  background: #292832 !important;
  border-color: #292832 !important;
}
button[kind="primary"]:hover { background: #484450 !important; }
.stTextInput input, .stTextArea textarea, .stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
  background: #fff !important;
  color: #292832 !important;
  border-color: #dfd6dc !important;
  border-radius: 10px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  color: #8a8189 !important;
}
.stRadio label, .stCheckbox label, .stSlider label, .stSelectbox label,
.stTextInput label, .stTextArea label, .stNumberInput label {
  color: #292832 !important;
}
[data-baseweb="tab-list"] { gap: 8px; }
button[data-baseweb="tab"] {
  color: #5a4b55 !important;
  border-radius: 10px 10px 0 0;
}
button[data-baseweb="tab"][aria-selected="true"] {
  color: #9b3f61 !important;
  border-bottom-color: #c66c8c !important;
}
.hero {
  position: relative; overflow: hidden;
  padding: clamp(28px, 5vw, 58px) clamp(22px, 5vw, 54px);
  border-radius: 30px;
  background: radial-gradient(circle at 88% 18%, rgba(255,255,255,.88) 0 8%, transparent 8.5%),
              radial-gradient(circle at 94% 78%, rgba(255,255,255,.45) 0 13%, transparent 13.5%),
              linear-gradient(120deg, #ffd8e6 0%, #fff0e7 52%, #f4c7d8 100%);
  border: 1px solid #efbfd0;
  box-shadow: 0 14px 38px rgba(145, 69, 99, .10);
  margin-bottom: 22px;
}
.hero h1 { color: #2e2430 !important; font-size: clamp(3rem, 8vw, 6.4rem); line-height: .98; letter-spacing: -3px; font-weight: 800; margin: 4px 0 0 0; }
.hero .studio { color: #a23e65; font-size: clamp(1rem, 2vw, 1.45rem); font-weight: 800; letter-spacing: .32em; margin-top: 12px; }
.hero p { color: #594550 !important; font-size: clamp(.95rem, 1.7vw, 1.12rem); margin: 13px 0 0 0; max-width: 650px; }
.hero .hero-note { color: #8b4964; font-size: .78rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; margin-top: 22px; }
.eyebrow {
  display: inline-block; background: #fff; color: #9b3f61;
  border: 1px solid #f0c6d5; padding: 5px 11px; border-radius: 999px;
  font-size: .78rem; font-weight: 800; letter-spacing: .5px; margin-bottom: 10px;
}
.section-title { font-size: 1.45rem; font-weight: 800; color: #302832; margin: 8px 0 4px; }
.product-card {
  background: #fff; border: 1px solid #f0dce3; border-radius: 18px;
  padding: 14px; box-shadow: 0 5px 20px rgba(90,40,60,.045);
}
.price { color: #a94769; font-weight: 800; font-size: 1.08rem; }
.pill {
  display:inline-block; padding:4px 9px; border-radius:999px;
  background:#fff0f5; color:#8e3e5b; font-size:.75rem; font-weight:700;
}
.notice {
  background:#fff; border-left:4px solid #c66c8c; border-radius:10px;
  padding:12px 15px; color:#39313a; margin:8px 0 14px;
}
.footer {
  text-align:center; color:#756873; padding:28px 0 12px; font-size:.85rem;
}
hr { border-color: #f0dce3 !important; }
[data-testid="stAlert"] { color: #292832 !important; }
@media (max-width: 700px) {
  .hero { padding: 24px 20px; }
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
MENU = [
    {"id":"ml01","name":"Trà sữa trân châu đường đen","category":"Trà sữa","price":39000,"tag":"Best seller","desc":"Trà sữa béo thơm, trân châu dai và sốt đường đen.","emoji":"🧋","image":"https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml02","name":"Trà sữa ô long kem cheese","category":"Trà sữa","price":42000,"tag":"Creamy","desc":"Ô long thơm nhẹ, lớp kem cheese mặn ngọt.","emoji":"🥤","image":"https://i.beauty321.com/600x/https%3A/il.beauty321.com/gallery/gallery/54522/photo-643e6356d2024.jpg"},
    {"id":"ml03","name":"Matcha latte","category":"Trà sữa","price":42000,"tag":"Green mood","desc":"Matcha thơm, vị đắng dịu và sữa mịn.","emoji":"🍵","image":"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml04","name":"Trà đào cam sả","category":"Trà trái cây","price":35000,"tag":"Fresh","desc":"Trà thanh mát, đào ngọt dịu, cam và sả thơm.","emoji":"🍑","image":"https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml05","name":"Trà gạo rang","category":"Trà nguyên bản","price":32000,"tag":"Gentle","desc":"Hương gạo rang ấm, hậu vị dịu và dễ uống.","emoji":"🌾","image":"https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml06","name":"Trà dưa lưới nhiệt đới","category":"Trà trái cây","price":36000,"tag":"Seasonal","desc":"Dưa lưới thơm ngọt kết hợp trà thanh mát.","emoji":"🍈","image":"https://bucket.cooklaif.com/311-honeydew-melon-iced-green-tea-311.jpg"},
    {"id":"ml07","name":"Cà phê sữa Ú Nu","category":"Cà phê","price":29000,"tag":"Wake up","desc":"Cà phê đậm đà, sữa ngọt vừa phải.","emoji":"☕","image":"https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml08","name":"Americano cam","category":"Cà phê","price":35000,"tag":"Bright","desc":"Cà phê thanh, hương cam tươi mát.","emoji":"🍊","image":"https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml09","name":"Trà sữa truyền thống Ú Nu","category":"Trà sữa","price":30000,"tag":"Classic","desc":"Trà đen đậm vị kết hợp sữa thơm béo, chuẩn gu truyền thống.","emoji":"🧋","image":"https://i.beauty321.com/600x/https%3A/il.beauty321.com/gallery/gallery/59587/photo-6597c97730efe.jpg"},
    {"id":"ml10","name":"Cacao latte macchiato","category":"Trà sữa","price":38000,"tag":"Chocolate mood","desc":"Cacao thơm đậm, sữa mịn và lớp kem béo nhẹ.","emoji":"🍫","image":"https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml11","name":"Trà xanh hoa nhài","category":"Trà nguyên bản","price":32000,"tag":"Floral","desc":"Hương hoa nhài dịu dàng, vị trà thanh mát dễ uống.","emoji":"🌸","image":"https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml12","name":"Trà Genmaicha gạo rang","category":"Trà nguyên bản","price":35000,"tag":"Japanese tea","desc":"Trà xanh Nhật Bản với hương gạo rang bùi thơm, hậu vị êm.","emoji":"🌾","image":"https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=900&q=85"},
    {"id":"ml13","name":"Sữa dâu giòn ngọt","category":"Trà trái cây","price":38000,"tag":"Pink favorite","desc":"Dâu chua ngọt kết hợp sữa dịu và topping dâu giòn vui miệng.","emoji":"🍓","image":"https://cdn.imweb.me/upload/S20221222519e961523905/883890a623fc4.jpg"},
]

TOPPINGS = {"Trân châu đen":7000,"Trân châu trắng":7000,"Pudding trứng":8000,"Kem cheese":10000,"Thạch trái cây":7000}
SIZES = {"M":0,"L":8000,"XL":15000}
SUGAR = ["0%","30%","50%","70%","100%"]
ICE = ["Không đá","Ít đá","Bình thường"]
VOUCHERS = {"MAMA10":10,"SWEET15":15,"HELLO20":10,"THUDUC20":20,"MAMALALA50":50,"XINCHAO":10}
STATUSES = ["Đã tiếp nhận","Đang pha chế","Sẵn sàng nhận","Đang giao","Hoàn tất","Đã hủy"]

# -------------------- SESSION STATE --------------------
defaults = {
    "cart": [], "orders": [], "reviews": [
        {"name":"Minh Thư","rating":5,"text":"Trà sữa đậm vị, trân châu dẻo ngon xuất sắc!","created_at":"17/10/2026"},
        {"name":"Gia Hân","rating":5,"text":"Quán xinh, đặt món tiện lợi và giao diện dễ thương.","created_at":"16/10/2026"},
    ], "points": 0,
    "used_vouchers": [], "active_voucher": "", "last_order_id": "",
    "passport": [], "admin_logged_in": False, "fortune_result": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def money(value):
    return f"{int(value):,}đ".replace(",", ".")

def get_product(product_id):
    return next((p for p in MENU if p["id"] == product_id), None)

def cart_subtotal():
    return sum(item["unit_price"] * item["qty"] for item in st.session_state.cart)

def cart_total():
    subtotal = cart_subtotal()
    discount = 0
    code = st.session_state.active_voucher
    if code in VOUCHERS:
        discount = int(subtotal * VOUCHERS[code] / 100)
    return max(0, subtotal - discount), discount

def fetch_image(url):
    """Download image and return a PIL image; failed URLs return None, never break the app."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent":"Mozilla/5.0"})
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.verify()
        response = requests.get(url, timeout=5, headers={"User-Agent":"Mozilla/5.0"})
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def cached_image(url):
    return fetch_image(url)

def add_to_cart(product, size, toppings, sugar, ice, note):
    topping_cost = sum(TOPPINGS[t] for t in toppings)
    unit_price = product["price"] + SIZES[size] + topping_cost
    key = str(uuid.uuid4())[:8]
    st.session_state.cart.append({
        "key": key, "id": product["id"], "name": product["name"],
        "size": size, "toppings": toppings, "sugar": sugar, "ice": ice,
        "note": note.strip(), "unit_price": unit_price, "qty": 1,
    })

def render_product_image(product, height=190):
    image = cached_image(product["image"])
    if image is not None:
        st.image(image, use_container_width=True)
    else:
        # Guaranteed readable fallback when an external image is unavailable.
        st.markdown(
            f"""<div style="height:{height}px;border-radius:14px;
            background:linear-gradient(135deg,#ffe4ed,#fff3e8);
            border:1px solid #f0d2dd;display:flex;align-items:center;
            justify-content:center;flex-direction:column;">
            <div style="font-size:4rem">{product['emoji']}</div>
            <div style="font-weight:800;color:#7d4058;margin-top:4px">{product['name']}</div>
            <div style="font-size:.8rem;color:#806c76">Tiệm trà Ú Nu • made with love</div></div>""",
            unsafe_allow_html=True
        )

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("# 🧋 Tiệm trà Ú Nu")
    st.markdown("**TEA • COFFEE • LITTLE JOY**")
    st.divider()
    st.markdown("### 🏡 Thông tin cửa hàng")
    st.markdown("📍 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức")
    st.markdown("🕒 08:00 – 22:30")
    st.markdown("☎️ 0987 123 456")
    st.caption("Thông tin cửa hàng là dữ liệu mẫu — hãy kiểm tra và thay bằng thông tin thật trước khi công khai website.")
    st.divider()
    st.markdown("### 🎡 Lucky Sip")
    st.write("Quay một lượt để nhận ưu đãi vui vẻ.")
    if st.button("🎁 QUAY NHẬN VOUCHER", use_container_width=True):
        possible = ["MAMA10","SWEET15","HELLO20"]
        st.session_state.fortune_result = random.choice(possible)
    if st.session_state.fortune_result:
        st.success(f"Bạn nhận được mã **{st.session_state.fortune_result}** giảm {VOUCHERS[st.session_state.fortune_result]}%!")
        if st.button("Dùng mã này", key="use_lucky_voucher", use_container_width=True):
            st.session_state.active_voucher = st.session_state.fortune_result
            st.rerun()
    st.markdown("### 🎟️ Mã giảm giá")
    code_input = st.text_input("Nhập mã voucher", placeholder="Ví dụ: MAMA10", key="voucher_input")
    if st.button("Áp dụng mã", use_container_width=True):
        normalized = code_input.strip().upper()
        if normalized in VOUCHERS:
            st.session_state.active_voucher = normalized
            st.success(f"Đã áp dụng {normalized}!")
        else:
            st.error("Mã chưa đúng. Thử MAMA10, SWEET15, HELLO20, THUDUC20, MAMALALA50 hoặc XINCHAO nhé.")
    if st.session_state.active_voucher:
        st.caption(f"Mã đang dùng: {st.session_state.active_voucher}")
        if st.button("Gỡ voucher", use_container_width=True):
            st.session_state.active_voucher = ""
            st.rerun()

# -------------------- HERO --------------------
# Nếu đặt TRASUA.jpg.JPG cùng thư mục với app.py, ảnh sẽ hiển thị ở đầu trang.
hero_image = Path(__file__).with_name("TRASUA.jpg.JPG")
if hero_image.exists():
    st.image(str(hero_image), use_container_width=True)

st.markdown("""
<div class="hero">
  <span class="eyebrow">WELCOME TO OUR LITTLE WORLD</span>
  <h1>Tiệm trà Ú Nu</h1>
  <div class="studio">TRÀ NGON · VUI MỖI NGÀY</div>
  <p>Một ngụm thơm ngon, một chút dịu dàng — ghé Ú Nu chọn món yêu thích và để ngày của bạn ngọt ngào hơn nhé!</p>
  <div class="hero-note">PHA BẰNG CẢ TẤM LÒNG · GỬI TRỌN NIỀM VUI</div>
</div>
""", unsafe_allow_html=True)

# -------------------- NAV TABS --------------------
tab_menu, tab_mood, tab_cart, tab_track, tab_reviews, tab_admin = st.tabs([
    "🧋 Menu", "💗 Mood Match", f"🛍️ Giỏ hàng ({sum(i['qty'] for i in st.session_state.cart)})",
    "📦 Theo dõi đơn", "⭐ Đánh giá", "🔐 Quản trị"
])

# -------------------- MENU --------------------
with tab_menu:
    left, right = st.columns([2,1])
    with left:
        st.markdown('<div class="section-title">Chọn món yêu thích</div>', unsafe_allow_html=True)
        st.caption("Tuỳ chỉnh size, topping và độ ngọt theo gu của bạn. Có 13 lựa chọn trà sữa, trà trái cây, trà nguyên bản và cà phê.")
    with right:
        category = st.selectbox("Danh mục", ["Tất cả"] + sorted({p["category"] for p in MENU}))
    search = st.text_input("🔎 Tìm món", placeholder="Nhập tên trà, cà phê...")
    filtered = [p for p in MENU if (category == "Tất cả" or p["category"] == category)
                and search.lower() in p["name"].lower()]
    if not filtered:
        st.info("Chưa tìm thấy món phù hợp. Thử từ khoá khác nhé.")
    for start in range(0, len(filtered), 2):
        cols = st.columns(2, gap="large")
        for col, product in zip(cols, filtered[start:start+2]):
            with col:
                with st.container(border=True):
                    render_product_image(product)
                    st.markdown(f"### {product['emoji']} {product['name']}")
                    st.markdown(f'<span class="pill">{product["tag"]}</span> &nbsp; <span class="price">{money(product["price"])}</span>', unsafe_allow_html=True)
                    st.write(product["desc"])
                    with st.form(f"form_{product['id']}"):
                        size = st.radio("Size", list(SIZES.keys()), horizontal=True, key=f"size_{product['id']}")
                        toppings = st.multiselect("Topping", list(TOPPINGS.keys()), key=f"top_{product['id']}")
                        sugar = st.select_slider("Đường", options=SUGAR, value="50%", key=f"sugar_{product['id']}")
                        ice = st.selectbox("Đá", ICE, key=f"ice_{product['id']}")
                        note = st.text_input("Ghi chú", placeholder="Ví dụ: ít ngọt hơn", key=f"note_{product['id']}")
                        price_preview = product["price"] + SIZES[size] + sum(TOPPINGS[t] for t in toppings)
                        st.markdown(f"**Tạm tính: {money(price_preview)}**")
                        if st.form_submit_button("＋ Thêm vào giỏ", use_container_width=True):
                            add_to_cart(product, size, toppings, sugar, ice, note)
                            st.success("Đã thêm món vào giỏ!")
                            st.rerun()

# -------------------- MOOD MATCH --------------------
with tab_mood:
    st.markdown('<div class="section-title">Hôm nay bạn đang cảm thấy thế nào?</div>', unsafe_allow_html=True)
    st.write("Tiệm trà Ú Nu gợi ý một món hợp mood của bạn 💕")
    mood = st.radio("Chọn mood", ["Cần tỉnh táo ⚡","Muốn thư giãn 🌿","Tâm trạng ngọt ngào 🍓","Muốn tươi mát 🍊"], horizontal=True)
    mood_map = {
        "Cần tỉnh táo ⚡":["Cà phê sữa Ú Nu","Americano cam"],
        "Muốn thư giãn 🌿":["Trà Genmaicha gạo rang","Matcha latte","Trà xanh hoa nhài"],
        "Tâm trạng ngọt ngào 🍓":["Trà sữa trân châu đường đen","Trà sữa ô long kem cheese","Sữa dâu giòn ngọt","Cacao latte macchiato"],
        "Muốn tươi mát 🍊":["Trà đào cam sả","Trà dưa lưới nhiệt đới","Trà xanh hoa nhài"],
    }
    suggested = [p for p in MENU if p["name"] in mood_map[mood]]
    for start in range(0, len(suggested), 3):
        cols = st.columns(3, gap="large")
        for col, product in zip(cols, suggested[start:start+3]):
            with col:
                with st.container(border=True):
                    render_product_image(product)
                    st.markdown(f"### {product['emoji']} {product['name']}")
                    st.markdown(f'<span class="price">{money(product["price"])}</span>', unsafe_allow_html=True)
                    st.write(product["desc"])
                    if st.button("Chọn món này", key=f"mood_{product['id']}", use_container_width=True):
                        add_to_cart(product, "M", [], "50%", "Ít đá", "")
                        st.success("Đã thêm size M vào giỏ.")
                        st.rerun()
    st.divider()
    st.markdown("### 🔮 Một lời nhắn nhỏ")
    fortunes = [
        "Bạn không cần hoàn hảo, chỉ cần tiến bộ từng chút một.",
        "Một khởi đầu nhỏ vẫn có thể tạo nên điều tuyệt vời.",
        "Hãy cho bản thân một khoảng nghỉ xứng đáng hôm nay.",
        "Điều tốt đẹp đôi khi bắt đầu từ một lựa chọn rất nhỏ."
    ]
    if st.button("Rút một lời nhắn"):
        st.info(random.choice(fortunes))


# -------------------- CART / CHECKOUT --------------------
with tab_cart:
    st.markdown('<div class="section-title">Giỏ hàng của bạn</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Ghé Menu để chọn món bạn thích nhé 🧋")
    else:
        remove_keys = []
        for item in st.session_state.cart:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3,1,1])
                with c1:
                    st.markdown(f"**{item['name']} — size {item['size']}**")
                    topping_text = ", ".join(item["toppings"]) if item["toppings"] else "Không topping"
                    st.caption(f"{topping_text} • {item['sugar']} đường • {item['ice']}")
                    if item["note"]:
                        st.caption(f"Ghi chú: {item['note']}")
                    st.write(f"Đơn giá: {money(item['unit_price'])}")
                with c2:
                    item["qty"] = st.number_input("SL", min_value=1, max_value=20, value=int(item["qty"]), key=f"qty_{item['key']}")
                with c3:
                    st.write("")
                    st.write("")
                    if st.button("🗑️ Xoá", key=f"remove_{item['key']}"):
                        remove_keys.append(item["key"])
                st.markdown(f"**Thành tiền: {money(item['unit_price'] * item['qty'])}**")
        if remove_keys:
            st.session_state.cart = [i for i in st.session_state.cart if i["key"] not in remove_keys]
            st.rerun()

        total, discount = cart_total()
        subtotal = cart_subtotal()
        a, b, c = st.columns(3)
        a.metric("Tạm tính", money(subtotal))
        b.metric("Giảm giá", f"-{money(discount)}")
        c.metric("Tổng thanh toán", money(total))
        if st.session_state.active_voucher:
            st.caption(f"Voucher áp dụng: {st.session_state.active_voucher} ({VOUCHERS[st.session_state.active_voucher]}%)")

        st.markdown("### 🧾 Thông tin nhận hàng")
        with st.form("checkout_form"):
            customer_name = st.text_input("Họ và tên", placeholder="Tên người nhận")
            phone = st.text_input("Số điện thoại", placeholder="09xxxxxxxx")
            method = st.radio("Hình thức nhận", ["Đến lấy tại cửa hàng","Giao hàng"], horizontal=True)
            address = st.text_input("Địa chỉ giao hàng", placeholder="Nhập địa chỉ (nếu chọn giao hàng)")
            payment = st.radio("Thanh toán", ["Tiền mặt khi nhận","Chuyển khoản (demo VietQR)"], horizontal=True)
            submitted = st.form_submit_button("🌸 Xác nhận đặt hàng", type="primary", use_container_width=True)
        if submitted:
            if not customer_name.strip() or not phone.strip():
                st.error("Bạn vui lòng nhập họ tên và số điện thoại.")
            elif method == "Giao hàng" and not address.strip():
                st.error("Bạn vui lòng nhập địa chỉ giao hàng.")
            else:
                order_id = "MAMA" + datetime.now().strftime("%y%m%d") + str(random.randint(100,999))
                order = {
                    "order_id": order_id, "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "name": customer_name.strip(), "phone": phone.strip(), "method": method,
                    "address": address.strip() if method == "Giao hàng" else "Nhận tại cửa hàng",
                    "payment": payment, "items": [dict(i) for i in st.session_state.cart],
                    "subtotal": subtotal, "discount": discount, "total": total,
                    "voucher": st.session_state.active_voucher, "status": "Đã tiếp nhận",
                }
                st.session_state.orders.insert(0, order)
                st.session_state.points += total // 1000
                st.session_state.passport.extend([i["name"] for i in st.session_state.cart])
                st.session_state.last_order_id = order_id
                st.session_state.cart = []
                st.session_state.active_voucher = ""
                st.success(f"Đặt hàng thành công! Mã đơn của bạn: **{order_id}**")
                st.rerun()

    # Always show the last order's payment details after rerun.
    last = next((o for o in st.session_state.orders if o["order_id"] == st.session_state.last_order_id), None)
    if last:
        st.divider()
        st.markdown("### ✅ Đơn hàng gần nhất")
        st.write(f"Mã đơn: **{last['order_id']}** • Trạng thái: **{last['status']}**")
        st.write(f"Tổng tiền: **{money(last['total'])}**")
        if "Chuyển khoản" in last["payment"]:
            st.markdown("### 💳 Thanh toán bằng VietQR")
            st.markdown(
                f'''<div style="background:#fff;border:1px solid #f0dce3;border-radius:18px;padding:16px 18px;margin:8px 0 14px;">
                  <div style="color:#8f4562;font-weight:800;font-size:.8rem;letter-spacing:.08em;">TIỆM TRÀ Ú NU · PAYMENT</div>
                  <div style="color:#2e2430;font-size:1.8rem;font-weight:800;margin:4px 0;">{money(last["total"])}</div>
                  <div style="color:#5f5660;">Nội dung chuyển khoản</div>
                  <div style="color:#2e2430;font-weight:800;font-size:1.05rem;">Thanh toan {last["order_id"]}</div>
                </div>''',
                unsafe_allow_html=True,
            )
            # Demo account placeholders only. Replace these with the shop's real bank details before launch.
            bank_id = "MB"
            account_no = "0123456789"
            account_name = "TIỆM TRÀ Ú NU DEMO"
            qr_url = (
                "https://img.vietqr.io/image/"
                f"{bank_id}-{account_no}-compact2.png?amount={last['total']}"
                f"&addInfo={quote('Thanh toan ' + last['order_id'])}"
                f"&accountName={quote(account_name)}"
            )
            qr_col, detail_col = st.columns([1, 1.35], gap="large")
            with qr_col:
                st.image(qr_url, caption="Quét mã QR để chuyển khoản (DEMO)", use_container_width=True)
            with detail_col:
                st.markdown("**Thông tin nhận tiền**")
                st.write("Ngân hàng: MB Bank (demo)")
                st.write(f"Số tài khoản: `{account_no}`")
                st.write(f"Tên tài khoản: `{account_name}`")
                st.write(f"Số tiền: **{money(last['total'])}**")
                st.write(f"Nội dung: **Thanh toan {last['order_id']}**")
                st.warning("QR và tài khoản hiện là dữ liệu minh hoạ, chưa nhận tiền thật. Hãy thay bằng tài khoản cửa hàng trước khi sử dụng thực tế.")
        else:
            st.info("Bạn đã chọn thanh toán tiền mặt khi nhận hàng. Vui lòng thanh toán tại cửa hàng hoặc khi nhận đồ.")
        st.caption("Lưu ý: bản demo lưu đơn trong phiên chạy Streamlit; khi khởi động lại, dữ liệu có thể mất.")

# -------------------- ORDER TRACKING --------------------
with tab_track:
    st.markdown('<div class="section-title">Theo dõi đơn hàng</div>', unsafe_allow_html=True)
    if not st.session_state.orders:
        st.info("Bạn chưa có đơn hàng nào trong phiên này.")
    else:
        order_ids = [o["order_id"] for o in st.session_state.orders]
        selected_id = st.selectbox("Chọn mã đơn", order_ids, index=0)
        order = next(o for o in st.session_state.orders if o["order_id"] == selected_id)
        st.markdown(f"### Đơn **{order['order_id']}**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng tiền", money(order["total"]))
        c2.metric("Hình thức", order["method"])
        c3.metric("Trạng thái", order["status"])
        st.caption(f"Người nhận: {order['name']} • {order['phone']} • Tạo lúc {order['created_at']}")
        st.write("**Sản phẩm**")
        for item in order["items"]:
            st.write(f"- {item['name']} (size {item['size']}) × {item['qty']} — {money(item['unit_price']*item['qty'])}")
        if order["status"] == "Đã hủy":
            st.error("Đơn hàng đã bị hủy.")
        else:
            progress_steps = STATUSES[:5]
            current_index = progress_steps.index(order["status"]) if order["status"] in progress_steps else 0
            st.progress((current_index + 1) / len(progress_steps))
            st.caption(" → ".join(progress_steps))


# -------------------- REVIEWS --------------------
with tab_reviews:
    st.markdown('<div class="section-title">Khách hàng nói gì?</div>', unsafe_allow_html=True)
    with st.form("review_form"):
        reviewer = st.text_input("Tên hiển thị", placeholder="Bạn có thể dùng biệt danh")
        rating = st.select_slider("Bạn chấm mấy sao?", options=[1,2,3,4,5], value=5)
        review_text = st.text_area("Chia sẻ trải nghiệm", placeholder="Món uống, dịch vụ hoặc góp ý của bạn...")
        review_submit = st.form_submit_button("Gửi đánh giá", use_container_width=True)
    if review_submit:
        if not review_text.strip():
            st.error("Bạn hãy viết vài dòng đánh giá trước khi gửi.")
        else:
            st.session_state.reviews.insert(0, {
                "name": reviewer.strip() or "Khách Tiệm trà Ú Nu",
                "rating": rating, "text": review_text.strip(),
                "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Cảm ơn bạn đã góp ý cho Tiệm trà Ú Nu!")
            st.rerun()
    st.divider()
    if not st.session_state.reviews:
        st.info("Chưa có đánh giá nào. Hãy là người đầu tiên nhé!")
    for review in st.session_state.reviews:
        with st.container(border=True):
            # Backward-compatible defaults for reviews saved by an older app version.
            name = review.get("name", "Khách Tiệm trà Ú Nu")
            rating = review.get("rating", 5)
            review_text = review.get(
                "text",
                review.get("comment", review.get("content", "Đánh giá chưa có nội dung"))
            )
            created_at = review.get("created_at", "Không rõ thời gian")
            try:
                rating = max(1, min(5, int(rating)))
            except (TypeError, ValueError):
                rating = 5
            st.markdown(f"**{name}**  ·  {'⭐' * rating}")
            st.write(review_text)
            st.caption(created_at)

# -------------------- ADMIN --------------------
with tab_admin:
    st.markdown('<div class="section-title">Khu vực quản trị</div>', unsafe_allow_html=True)
    if not st.session_state.admin_logged_in:
        st.info("Đăng nhập để xem đơn hàng và số liệu demo.")
        with st.form("admin_login_form"):
            password = st.text_input("Mật khẩu quản trị", type="password")
            login = st.form_submit_button("Đăng nhập", type="primary")
        if login:
            # Demo password only. Use Streamlit secrets/environment variables in production.
            if password == st.secrets.get("ADMIN_PASSWORD", "mama2026"):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Mật khẩu chưa đúng.")
    else:
        top1, top2 = st.columns([3,1])
        with top1:
            st.success("Đã đăng nhập quản trị (demo).")
        with top2:
            if st.button("Đăng xuất"):
                st.session_state.admin_logged_in = False
                st.rerun()
        orders = st.session_state.orders
        revenue = sum(o["total"] for o in orders if o["status"] != "Đã hủy")
        completed = sum(1 for o in orders if o["status"] == "Hoàn tất")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tổng đơn", len(orders))
        m2.metric("Doanh thu demo", money(revenue))
        m3.metric("Đơn hoàn tất", completed)
        m4.metric("Đánh giá", len(st.session_state.reviews))
        if orders:
            st.markdown("### 📦 Quản lý đơn hàng")
            for order in orders:
                with st.container(border=True):
                    c1, c2 = st.columns([3,2])
                    with c1:
                        st.markdown(f"**{order['order_id']} — {order['name']}**")
                        st.caption(f"{order['created_at']} • {order['phone']} • {order['method']}")
                        st.write(f"{money(order['total'])} • {len(order['items'])} dòng sản phẩm")
                    with c2:
                        current = order["status"]
                        new_status = st.selectbox(
                            "Trạng thái", STATUSES,
                            index=STATUSES.index(current),
                            key=f"status_{order['order_id']}"
                        )
                        if st.button("Lưu trạng thái", key=f"save_{order['order_id']}", use_container_width=True):
                            order["status"] = new_status
                            st.success("Đã cập nhật trạng thái.")
                            st.rerun()
            export_rows = []
            for order in orders:
                export_rows.append({
                    "Mã đơn": order["order_id"], "Ngày tạo": order["created_at"],
                    "Khách hàng": order["name"], "SĐT": order["phone"],
                    "Hình thức": order["method"], "Thanh toán": order["payment"],
                    "Trạng thái": order["status"], "Tạm tính": order["subtotal"],
                    "Giảm giá": order["discount"], "Tổng tiền": order["total"],
                })
            csv = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Xuất danh sách đơn hàng (CSV)", csv, "tien_tra_u_nu_orders.csv", "text/csv")
            all_items = []
            for order in orders:
                if order["status"] != "Đã hủy":
                    for item in order["items"]:
                        all_items.extend([item["name"]] * item["qty"])
            if all_items:
                st.markdown("### 🏆 Món được gọi nhiều")
                counts = pd.Series(all_items).value_counts().head(5)
                st.bar_chart(counts)
        else:
            st.info("Chưa có đơn hàng nào trong phiên chạy này.")

st.markdown('<div class="footer">🧋 Tiệm trà Ú Nu · Trà ngon, vui mỗi ngày<br>Chọn món yêu thích · Tuỳ chỉnh theo gu · Gửi trọn niềm vui</div>', unsafe_allow_html=True)
