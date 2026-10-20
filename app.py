import streamlit as st
import pandas as pd
import random
import string
import json
import os
from datetime import datetime
from urllib.parse import quote

# =========================================================
# CẤU HÌNH
# =========================================================
st.set_page_config(
    page_title="Tiệm trà Ú nu | Tea • Coffee • Little Joy",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bạn có thể thay các URL ảnh bằng ảnh sản phẩm của quán.
MENU = {
    "Trà sữa trân châu đường đen": {
        "price": 39000, "category": "Trà sữa", "tag": "Best seller",
        "desc": "Trà sữa béo thơm, trân châu dai và sốt đường đen đậm vị.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
        "mood": ["Cần năng lượng", "Muốn được vỗ về", "Vui vẻ"],
    },
    "Trà sữa ô long kem cheese": {
        "price": 42000, "category": "Trà sữa", "tag": "Creamy",
        "desc": "Ô long thơm nhẹ, lớp kem cheese mặn ngọt mềm mịn.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn được vỗ về", "Cần thư giãn"],
    },
    "Trà sữa matcha": {
        "price": 38000, "category": "Trà sữa", "tag": "Matcha",
        "desc": "Matcha thơm dịu, vị trà rõ và hậu vị thanh.",
        "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85",
        "mood": ["Cần tập trung", "Cần thư giãn"],
    },
    "Trà sữa thái xanh": {
        "price": 35000, "category": "Trà sữa", "tag": "Fresh",
        "desc": "Thái xanh thơm béo, ngọt dịu và dễ uống.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
        "mood": ["Vui vẻ", "Muốn được vỗ về"],
    },
    "Trà sữa dâu tây": {
        "price": 36000, "category": "Trà sữa", "tag": "Fruity",
        "desc": "Hương dâu tươi vui, ngọt thơm và có màu sắc bắt mắt.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
        "mood": ["Vui vẻ", "Muốn đổi gió"],
    },
    "Trà sữa khoai môn": {
        "price": 36000, "category": "Trà sữa", "tag": "Popular",
        "desc": "Khoai môn thơm bùi, vị ngọt mềm và béo vừa.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn được vỗ về", "Cần thư giãn"],
    },
    "Trà đào cam sả": {
        "price": 35000, "category": "Trà trái cây", "tag": "Refreshing",
        "desc": "Đào ngọt thơm kết hợp cam và sả thơm mát.",
        "image": "https://images.unsplash.com/photo-1513558161293-c2b9a9f9b3f5?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn đổi gió", "Cần thư giãn", "Nóng nực"],
    },
    "Trà vải hoa hồng": {
        "price": 37000, "category": "Trà trái cây", "tag": "Floral",
        "desc": "Vải thơm ngọt cùng hương hoa hồng dịu nhẹ.",
        "image": "https://images.unsplash.com/photo-1513558161293-c2b9a9f9b3f5?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn đổi gió", "Vui vẻ"],
    },
    "Trà chanh dây": {
        "price": 32000, "category": "Trà trái cây", "tag": "Tangy",
        "desc": "Chua ngọt sảng khoái, hợp những ngày cần tỉnh táo.",
        "image": "https://images.unsplash.com/photo-1513558161293-c2b9a9f9b3f5?auto=format&fit=crop&w=900&q=85",
        "mood": ["Nóng nực", "Cần năng lượng"],
    },
    "Trà dâu tằm": {
        "price": 33000, "category": "Trà trái cây", "tag": "Berry",
        "desc": "Dâu tằm chua ngọt nhẹ, màu sắc hấp dẫn.",
        "image": "https://images.unsplash.com/photo-1513558161293-c2b9a9f9b3f5?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn đổi gió", "Vui vẻ"],
    },
    "Americano": {
        "price": 30000, "category": "Cà phê", "tag": "Coffee",
        "desc": "Cà phê đậm vị, phù hợp khi cần tập trung.",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=85",
        "mood": ["Cần tập trung", "Cần năng lượng"],
    },
    "Latte": {
        "price": 39000, "category": "Cà phê", "tag": "Smooth",
        "desc": "Espresso hòa quyện sữa tươi, vị cân bằng.",
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=85",
        "mood": ["Muốn được vỗ về", "Cần thư giãn"],
    },
    "Cacao sữa": {
        "price": 35000, "category": "Khác", "tag": "Chocolate",
        "desc": "Cacao thơm, ngọt béo vừa phải.",
