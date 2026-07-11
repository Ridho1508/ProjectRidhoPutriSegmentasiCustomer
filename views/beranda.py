import streamlit as st

from utils.styling import hero, CLUSTER_META, goto, svg_icon
from utils.model_loader import load_models


def render():
    scaler, kmeans, cluster_labels = load_models()

    # ------------------------------------------------------------------
    # HERO
    # ------------------------------------------------------------------
    hero(
        eyebrow="Customer Intelligence · K-Means",
        title="Peta Segmen Pelanggan Grosir Anda",
        subtitle=(
            "Model K-Means membagi pelanggan menjadi 3 segmen berdasarkan pola belanja "
            "tahunan di 6 kategori produk. Pilih salah satu menu di bawah untuk memprediksi "
            "satu pelanggan, memproses banyak data sekaligus, atau menjelajahi dashboard."
        ),
    )

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # RINGKASAN MODEL
    # ------------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jumlah Segmen", f"{kmeans.n_clusters}")
    with col2:
        st.metric("Fitur yang Dipakai", "6 kategori")
    with col3:
        st.metric("Algoritma", "K-Means")
    with col4:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.045); border:1px solid rgba(255,255,255,0.09); border-radius:14px; padding:0.9rem 1.1rem 0.7rem 1.1rem;">
                <div style="font-size:0.875rem; color:#A9ADBE; margin-bottom:0.2rem;">Status Model</div>
                <div class="status-badge" style="font-size:1.6rem; font-weight:600;">
                    Siap Pakai
                    <span class="dot">{svg_icon('check')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # ------------------------------------------------------------------
    # KARTU 3 SEGMEN
    # ------------------------------------------------------------------
    st.subheader("Tiga Segmen yang Ditemukan Model")
    cols = st.columns(3)
    for i, col in enumerate(cols):
        meta = CLUSTER_META[i]
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="border-top: 3px solid {meta['color']}; box-shadow: 0 0 0 1px {meta['color']}22, 0 10px 28px -14px {meta['color']}66;">
                    <div style="font-size:1.8rem; color:{meta['color']};">{meta['icon_svg']}</div>
                    <h4 style="font-family:'Sora',sans-serif; margin:0.5rem 0 0.3rem 0; color:{meta['color']};">
                        {cluster_labels[i]}
                    </h4>
                    <p style="color:#A9ADBE; font-size:0.9rem; line-height:1.55; margin:0;">
                        {meta['desc']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # NAVIGASI FITUR — kartu yang bisa langsung dipencet di tengah halaman
    # ------------------------------------------------------------------
    st.subheader("Mau Mulai dari Mana?")
    nav_cols = st.columns(4)
    nav_items = [
        (svg_icon("predict"), "Prediksi Manual", "Masukkan data satu pelanggan lewat form, langsung lihat segmennya.", "prediksi"),
        (svg_icon("upload"), "Upload Massal", "Upload CSV berisi banyak pelanggan, dapatkan hasil & insight sekaligus.", "upload"),
        (svg_icon("chart"), "Dashboard", "Jelajahi karakteristik tiap segmen lewat grafik interaktif.", "dashboard"),
        (svg_icon("info"), "Tentang Proyek", "Penjelasan proyek ini dan siapa yang membuatnya.", "tentang"),
    ]
    for col, (icon, title, desc, target) in zip(nav_cols, nav_items):
        with col:
            st.markdown(
                f"""
                <div class="nav-card">
                    <div class="icon">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Buka {title} →", key=f"home_nav_{target}", use_container_width=True):
                goto(target)

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    with st.expander("Tentang dataset & fitur yang digunakan"):
        st.markdown(
            """
            Model ini dilatih dari data **belanja tahunan pelanggan grosir** pada 6 kategori produk:

            - 🥬 **Fresh** — produk segar
            - 🥛 **Milk** — susu & olahannya
            - 🛒 **Grocery** — kebutuhan grosir umum
            - 🧊 **Frozen** — produk beku
            - 🧴 **Detergents & Paper** — deterjen & produk kertas
            - 🍱 **Delicassen** — makanan siap saji

            Nilainya dinormalisasi dengan **StandardScaler**, lalu dikelompokkan dengan
            **K-Means (k=3)** menjadi tiga segmen: *Grosir*, *Reguler*, dan *Premium*.
            """
        )
