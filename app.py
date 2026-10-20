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
