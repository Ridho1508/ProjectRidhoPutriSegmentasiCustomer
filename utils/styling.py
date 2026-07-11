"""
styling.py
-----------
Semua hal yang berkaitan dengan tampilan (tema dark glassmorphism, warna khas
Nusa Putra University) dikumpulkan di sini supaya file halaman (app.py,
views/*.py) tetap fokus ke logika, bukan CSS.
"""

import base64
from pathlib import Path

import streamlit as st

# ------------------------------------------------------------------
# TOKEN DESAIN (satu sumber kebenaran untuk warna & style)
# Palet dasar tetap dark, tapi aksen warnanya diambil dari identitas
# kampus Nusa Putra University (magenta & plum di logo).
# ------------------------------------------------------------------
COLORS = {
    "bg_top": "#120A14",
    "bg_bottom": "#0B0710",
    "surface": "rgba(255,255,255,0.045)",
    "surface_border": "rgba(255,255,255,0.09)",
    "text": "#ECEEF6",
    "text_muted": "#A9ADBE",
    "campus_pink": "#E85D9A",    # Premium / aksen utama (magenta terang logo)
    "campus_rose": "#C2185B",    # aksen tombol / gradient
    "campus_plum": "#7E0048",    # Grosir / plum gelap logo
    "teal": "#35D6A5",           # Reguler (kontras penyeimbang, tetap dipertahankan)
    "danger": "#F0637C",
}

LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo_nusa_putra_web.png"
WATERMARK_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo_watermark.png"


def _logo_base64() -> str | None:
    """Baca logo kampus dari assets/ dan encode ke base64 supaya bisa ditaruh inline di HTML."""
    if not LOGO_PATH.exists():
        return None
    return base64.b64encode(LOGO_PATH.read_bytes()).decode()


def _watermark_base64() -> str | None:
    """
    Baca versi watermark logo (opacity sudah dibakar langsung ke channel alpha
    gambarnya, ~4-5%). Sengaja dipakai file terpisah dari logo di brand-bar,
    supaya opacity-nya tidak perlu diatur lewat CSS.
    """
    if not WATERMARK_PATH.exists():
        return None
    return base64.b64encode(WATERMARK_PATH.read_bytes()).decode()


# ------------------------------------------------------------------
# IKON GARIS (line icon) — pengganti emoji supaya tampilan lebih premium
# dan konsisten warnanya dengan tema. Pakai width/height "1em" supaya
# ukurannya otomatis ikut font-size elemen pembungkusnya (gampang diatur
# tanpa perlu bikin fungsi dengan parameter ukuran).
# ------------------------------------------------------------------
SVG_ICONS = {
    "store": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M3 7h18l-1.5 12a2 2 0 0 1-2 1.8H6.5a2 2 0 0 1-2-1.8L3 7z"/><path d="M8 7V5a4 4 0 0 1 8 0v2"/></svg>',
    "basket": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M4 10h16l-1.6 9.2a2 2 0 0 1-2 1.8H7.6a2 2 0 0 1-2-1.8L4 10z"/><path d="M8 10 6 4M16 10l2-6M9 14v3M15 14v3"/></svg>',
    "crown": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M3 8l4 3 5-6 5 6 4-3-2 11H5L3 8z"/></svg>',
    "home": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/></svg>',
    "predict": '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-0.15em;"><path d="M12 2l1.5 6.5L20 10l-6.5 1.5L12 18l-1.5-6.5L4 10l6.5-1.5L12 2z"/></svg>',
    "upload": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/></svg>',
    "chart": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><path d="M4 20V10M12 20V4M20 20v-7"/></svg>',
    "info": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-0.15em;"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg>',
    "check": '<svg width="1em" height="1em" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>',
}


def svg_icon(name: str) -> str:
    """Ambil markup SVG ikon garis berdasarkan nama. Kembalikan string kosong kalau nama tidak ada."""
    return SVG_ICONS.get(name, "")


# Metadata tiap cluster: warna, ikon, deskripsi singkat (bahasa bisnis, bukan statistik)
CLUSTER_META = {
    0: {
        "color": COLORS["campus_plum"],
        "icon": "🏪",
        "icon_svg": svg_icon("store"),
        "short": "Grosir",
        "desc": "Belanja rutin dalam volume besar, dominan di Susu, Groceries, dan Deterjen/Kertas — pola khas toko/ritel.",
    },
    1: {
        "color": COLORS["teal"],
        "icon": "🧺",
        "icon_svg": svg_icon("basket"),
        "short": "Reguler",
        "desc": "Pola belanja moderat dan stabil di semua kategori — mencerminkan pelanggan harian pada umumnya.",
    },
    2: {
        "color": COLORS["campus_pink"],
        "icon": "👑",
        "icon_svg": svg_icon("crown"),
        "short": "Premium",
        "desc": "Volume belanja sangat tinggi terutama di Fresh, Frozen, dan Delicassen — pelanggan bernilai tinggi (horeca/resto besar).",
    },
}


def inject_base_css():
    # PENTING: tidak boleh ada baris kosong di dalam blok <style>...</style>.
    # Kalau ada baris kosong, parser markdown Streamlit akan menganggap blok HTML
    # sudah selesai di tengah jalan, lalu sisa CSS malah dirender sebagai teks biasa
    # di halaman (bug yang sempat muncul). Makanya semua rule digabung rapat tanpa gap.
    #
    # CATATAN PERBAIKAN BUG (watermark menutupi seluruh halaman):
    # Versi sebelumnya menaruh watermark logo lewat pseudo-element ".stApp::before"
    # dengan position:fixed + z-index. Ternyata elemen "positioned" seperti itu
    # selalu digambar DI ATAS konten normal yang tidak diberi posisi -- walaupun
    # z-index-nya kecil dan walaupun opacity-nya rendah -- sehingga watermark-nya
    # malah menutupi seluruh nav & isi halaman. Sekarang watermark ditaruh sebagai
    # salah satu layer di properti "background" milik .stApp itu sendiri (bukan
    # pseudo-element terpisah), supaya otomatis tergambar di belakang semua anak
    # elemen tanpa perlu utak-atik z-index sama sekali. Opacity-nya juga sudah
    # "dibakar" langsung ke channel alpha gambarnya (lihat assets/logo_watermark.png),
    # bukan diatur lewat CSS opacity, supaya tidak ada trik tambahan yang bisa gagal.
    logo_b64 = _logo_base64()
    watermark_b64 = _watermark_base64()

    bg_images = [
        f"radial-gradient(circle at 10% -5%, {COLORS['campus_pink']}38 0%, transparent 40%)",
        f"radial-gradient(circle at 92% 8%, {COLORS['campus_plum']}55 0%, transparent 38%)",
        f"radial-gradient(circle at 50% 105%, {COLORS['campus_rose']}30 0%, transparent 45%)",
    ]
    bg_positions = ["0 0", "0 0", "0 0"]
    bg_sizes = ["auto", "auto", "auto"]
    bg_repeats = ["no-repeat", "no-repeat", "no-repeat"]

    if watermark_b64:
        bg_images.append(f"url('data:image/png;base64,{watermark_b64}')")
        bg_positions.append("center center")
        bg_sizes.append("55% auto")
        bg_repeats.append("no-repeat")

    # Layer paling bawah: warna dasar gelap (harus paling akhir di daftar).
    bg_images.append(f"linear-gradient(180deg, {COLORS['bg_top']} 0%, {COLORS['bg_bottom']} 100%)")
    bg_positions.append("0 0")
    bg_sizes.append("auto")
    bg_repeats.append("no-repeat")

    stapp_background = (
        f".stApp {{ color: {COLORS['text']}; "
        f"background-image: {', '.join(bg_images)}; "
        f"background-position: {', '.join(bg_positions)}; "
        f"background-size: {', '.join(bg_sizes)}; "
        f"background-repeat: {', '.join(bg_repeats)}; "
        f"background-attachment: fixed; }}"
    )

    css_rules = [
        "html, body, [class*=\"css\"] { font-family: 'Inter', sans-serif; }",
        "/* Background: ambient glow warna kampus + watermark logo, semua sebagai layer background biasa */",
        "html, body { background: transparent !important; }",
        stapp_background,
        "/* Sidebar dinonaktifkan sepenuhnya: navigasi memakai menu tengah, bukan sidebar */",
        "section[data-testid=\"stSidebar\"] { display: none; }",
        "div[data-testid=\"collapsedControl\"] { display: none; }",
        "/* Bar brand kecil di atas menu navigasi (berisi logo kampus) */",
        f".brand-bar {{ text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: {COLORS['text_muted']}; padding-top: 0.6rem; margin-bottom: 0.3rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }}",
        f".brand-bar b {{ color: {COLORS['campus_pink']}; font-weight: 600; }}",
        f".brand-logo {{ height: 28px; width: auto; vertical-align: middle; filter: drop-shadow(0 0 6px {COLORS['campus_pink']}70); }}",
        "/* Wrapper navigasi tengah (segmented control, pengganti sidebar) */",
        ".st-key-topnav { width: 100%; margin: 0 auto 1.8rem auto; }",
        ".st-key-topnav, .st-key-topnav > div, .st-key-topnav [data-testid=\"stVerticalBlockBorderWrapper\"], .st-key-topnav [data-testid=\"stVerticalBlock\"], .st-key-topnav [data-testid=\"stElementContainer\"] { display: flex !important; justify-content: center !important; width: 100% !important; }",
        ".st-key-topnav button { border-radius: 999px !important; font-family: 'Sora', sans-serif !important; transition: box-shadow 0.2s ease; }",
        f".st-key-topnav button[aria-checked=\"true\"] {{ box-shadow: 0 0 20px {COLORS['campus_rose']}70, 0 0 3px {COLORS['campus_rose']}; }}",
        "/* Typography */",
        "h1, h2, h3 { font-family: 'Sora', sans-serif !important; letter-spacing: -0.01em; }",
        "h1 { font-weight: 800 !important; }",
        "h2, h3 { font-weight: 700 !important; }",
        f"p, li, span, label {{ color: {COLORS['text']}; }}",
        "/* Glass card */",
        f".glass-card {{ background: {COLORS['surface']}; border: 1px solid {COLORS['surface_border']}; border-radius: 18px; padding: 1.4rem 1.6rem; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); margin-bottom: 1rem; transition: border-color 0.25s ease, box-shadow 0.25s ease; }}",
        f".glass-card:hover {{ border-color: {COLORS['campus_pink']}70; box-shadow: 0 0 24px {COLORS['campus_pink']}22; }}",
        "/* Hero */",
        f".hero-eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: {COLORS['campus_pink']}; margin-bottom: 0.4rem; }}",
        ".hero-title { font-family: 'Sora', sans-serif; font-size: 2.6rem; font-weight: 800; line-height: 1.15; background: linear-gradient(90deg, #FFFFFF 20%, #D9AFC6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.6rem; }",
        f".hero-sub {{ color: {COLORS['text_muted']}; font-size: 1.02rem; max-width: 640px; line-height: 1.6; }}",
        "/* Badge cluster */",
        ".badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.32rem 0.85rem; border-radius: 999px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 500; border: 1px solid rgba(255,255,255,0.14); }",
        "/* Status badge premium (pengganti emoji ceklis) */",
        ".status-badge { display: inline-flex; align-items: center; gap: 0.45rem; font-family: 'Sora', sans-serif; }",
        ".status-badge .dot { width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #35D6A5, #1F9E78); box-shadow: 0 0 12px rgba(53,214,165,0.6); flex-shrink: 0; }",
        ".status-badge .dot svg { color: #06231A; }",
        "/* Metric override */",
        f"div[data-testid=\"stMetric\"] {{ background: {COLORS['surface']}; border: 1px solid {COLORS['surface_border']}; border-radius: 14px; padding: 0.9rem 1.1rem 0.6rem 1.1rem; }}",
        f"div[data-testid=\"stMetricValue\"] {{ font-family: 'JetBrains Mono', monospace; color: {COLORS['text']}; }}",
        f"div[data-testid=\"stMetricLabel\"] {{ color: {COLORS['text_muted']}; }}",
        "/* Buttons */",
        f".stButton > button, .stDownloadButton > button {{ background: linear-gradient(135deg, {COLORS['campus_rose']} 0%, {COLORS['campus_plum']} 100%); color: #FFFFFF; font-weight: 700; border: none; border-radius: 10px; padding: 0.55rem 1.3rem; transition: transform 0.15s ease, box-shadow 0.15s ease; }}",
        f".stButton > button:hover, .stDownloadButton > button:hover {{ transform: translateY(-1px); box-shadow: 0 6px 18px {COLORS['campus_rose']}55; color: #FFFFFF; }}",
        "/* Nav cards on Home */",
        f".nav-card {{ display: block; padding: 1.3rem; border-radius: 16px; background: {COLORS['surface']}; border: 1px solid {COLORS['surface_border']}; height: 100%; transition: border-color 0.2s ease, box-shadow 0.2s ease; }}",
        f".nav-card:hover {{ border-color: {COLORS['campus_pink']}80; box-shadow: 0 0 26px {COLORS['campus_pink']}30; }}",
        f".nav-card .icon {{ font-size: 1.5rem; color: {COLORS['campus_pink']}; }}",
        ".nav-card h4 { font-family: 'Sora', sans-serif; margin: 0.5rem 0 0.25rem 0; font-size: 1.08rem; }",
        f".nav-card p {{ color: {COLORS['text_muted']}; font-size: 0.88rem; margin: 0; line-height: 1.5; }}",
        "/* Divider */",
        f".thin-divider {{ height: 1px; background: linear-gradient(90deg, transparent, {COLORS['campus_pink']}55, transparent); border: none; margin: 1.6rem 0; }}",
        "footer {visibility: hidden;}",
        "#MainMenu {visibility: hidden;}",
        "/* Kartu tim / kredit pembuat (halaman Tentang) */",
        f".team-card {{ display: flex; align-items: center; gap: 1rem; background: {COLORS['surface']}; border: 1px solid {COLORS['surface_border']}; border-radius: 18px; padding: 1.2rem 1.4rem; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); margin-bottom: 1rem; }}",
        ".team-avatar { flex-shrink: 0; width: 54px; height: 54px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.15rem; color: #FFFFFF; }",
        ".team-name { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.02rem; margin: 0; }",
        f".team-nim {{ font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: {COLORS['text_muted']}; margin: 0.15rem 0 0 0; }}",
        "/* Chip kecil untuk stack teknologi di halaman Tentang */",
        f".tech-chip {{ display: inline-flex; align-items: center; gap: 0.35rem; background: {COLORS['surface']}; border: 1px solid {COLORS['surface_border']}; border-radius: 999px; padding: 0.3rem 0.8rem; font-size: 0.82rem; margin: 0.2rem 0.3rem 0.2rem 0; color: {COLORS['text']}; }}",
    ]
    css = "\n".join(css_rules)

    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def hero(eyebrow: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-eyebrow">{eyebrow}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def badge(cluster_id: int, size: str = "normal") -> str:
    meta = CLUSTER_META[cluster_id]
    return (
        f'<span class="badge" style="background:{meta["color"]}22; '
        f'color:{meta["color"]}; border-color:{meta["color"]}55;">'
        f'{meta["icon_svg"]} {meta["short"]}</span>'
    )


# Ikon di menu navigasi pakai shortcode Material Symbols bawaan Streamlit
# (":material/nama_ikon:") — didukung langsung oleh st.segmented_control lewat
# format_func, hasilnya ikon garis konsisten tanpa perlu HTML custom.
PAGES = {
    "beranda": {"icon": ":material/home:", "label": "Beranda"},
    "prediksi": {"icon": ":material/auto_awesome:", "label": "Prediksi Manual"},
    "upload": {"icon": ":material/upload_file:", "label": "Upload Massal"},
    "dashboard": {"icon": ":material/bar_chart:", "label": "Dashboard"},
    "tentang": {"icon": ":material/info:", "label": "Tentang"},
}


def goto(page_key: str):
    """
    Pindah halaman secara terprogram (dipanggil dari tombol/kartu di dalam halaman).

    CATATAN PENTING (perbaikan bug):
    Kita TIDAK boleh langsung menimpa st.session_state["nav_widget"] di sini,
    karena widget dengan key "nav_widget" sudah "dipakai" lebih dulu di run yang
    sama (top_nav() selalu dipanggil sebelum halaman lain dirender). Streamlit
    melarang perubahan session_state milik sebuah widget setelah widget itu
    diinstansiasi di run yang sama -> itulah yang menyebabkan
    StreamlitAPIException kemarin.

    Solusinya: simpan tujuan halaman ke key sementara ("_pending_nav"), lalu
    rerun. Di run berikutnya, top_nav() akan menerapkan "_pending_nav" ke
    "nav_widget" SEBELUM widget-nya dibuat -> ini diperbolehkan Streamlit.
    """
    st.session_state["_pending_nav"] = page_key
    st.rerun()


def top_nav() -> str:
    """
    Render menu navigasi utama di tengah halaman (pengganti sidebar bawaan Streamlit).
    Mengembalikan key halaman yang sedang aktif.
    """
    # Terapkan navigasi yang "dititipkan" oleh goto(), sebelum widget dibuat.
    if "_pending_nav" in st.session_state:
        st.session_state["nav_widget"] = st.session_state.pop("_pending_nav")

    if "nav_widget" not in st.session_state:
        st.session_state.nav_widget = "beranda"

    logo_b64 = _logo_base64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo">' if logo_b64 else svg_icon("store")
    )
    st.markdown(
        f'<div class="brand-bar">{logo_html} <b>Wholesale Customer Intelligence</b> · Nusa Putra University</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="topnav"):
        selection = st.segmented_control(
            "Navigasi utama",
            options=list(PAGES.keys()),
            format_func=lambda k: f"{PAGES[k]['icon']}  {PAGES[k]['label']}",
            key="nav_widget",
            label_visibility="collapsed",
        )

    if selection is not None:
        st.session_state.active_page = selection
    elif "active_page" not in st.session_state:
        st.session_state.active_page = "beranda"

    return st.session_state.active_page


def glass_open():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def glass_close():
    st.markdown("</div>", unsafe_allow_html=True)
