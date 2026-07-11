`import streamlit as st

from utils.styling import inject_base_css, top_nav
from views import beranda, prediksi_manual, upload_massal, dashboard, tentang

st.set_page_config(
    page_title="Segmentasi Pelanggan | Wholesale Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_base_css()

# Inisialisasi "memori" sesi untuk menampung riwayat prediksi dari halaman lain
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------------------------------
# NAVIGASI UTAMA — menu langsung di tengah halaman, tanpa sidebar
# ------------------------------------------------------------------
active_page = top_nav()

PAGE_RENDERERS = {
    "beranda": beranda.render,
    "prediksi": prediksi_manual.render,
    "upload": upload_massal.render,
    "dashboard": dashboard.render,
    "tentang": tentang.render,
}

PAGE_RENDERERS.get(active_page, beranda.render)()
