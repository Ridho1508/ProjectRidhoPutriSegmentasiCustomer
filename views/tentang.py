import streamlit as st

from utils.styling import hero, glass_open, glass_close, CLUSTER_META, goto

TEAM = [
    {"name": "Ridho Safutra", "nim": "20240040121", "initials": "RS", "color": "#C2185B"},
    {"name": "Putri Prisilia", "nim": "20240040110", "initials": "PP", "color": "#7E0048"},
]

TECH_STACK = [
    ("🐍", "Python"),
    ("🎈", "Streamlit"),
    ("🤖", "scikit-learn"),
    ("📈", "Plotly"),
    ("🐼", "Pandas & NumPy"),
]


def render():
    hero(
        eyebrow="Tentang",
        title="Cerita di Balik Proyek Ini",
        subtitle="Sedikit latar belakang tentang apa yang coba dijawab aplikasi ini, dan siapa yang membangunnya.",
    )
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    left, right = st.columns([1.3, 1])

    with left:
        glass_open()
        st.markdown("##### 🎯 Masalah yang Diselesaikan")
        st.markdown(
            """
            Sebuah bisnis grosir mencatat belanja tahunan pelanggannya di 6 kategori produk,
            tapi kesulitan membaca pola di baliknya: siapa pelanggan bervolume besar seperti toko,
            siapa yang belanjanya moderat dan rutin, dan siapa yang tergolong bernilai tinggi (premium).

            Alih-alih menebak secara manual, proyek ini melatih model **unsupervised learning**
            untuk menemukan pengelompokan itu sendiri dari data — lalu membungkusnya menjadi
            aplikasi web yang bisa dipakai siapa saja tanpa perlu menyentuh kode.
            """
        )
        glass_close()

        glass_open()
        st.markdown("##### ⚙️ Cara Kerja Model")
        st.markdown(
            """
            1. **Data mentah** — belanja tahunan pelanggan grosir di kategori Fresh, Milk, Grocery,
               Frozen, Detergents & Paper, dan Delicassen.
            2. **Standardisasi** — nilai dinormalisasi dengan `StandardScaler` agar kategori dengan
               skala besar (mis. Fresh) tidak mendominasi kategori dengan skala kecil.
            3. **Clustering** — algoritma **K-Means (k=3)** mengelompokkan pelanggan berdasarkan
               kemiripan pola belanja ke 3 pusat cluster.
            4. **Pelabelan bisnis** — tiap cluster diberi nama yang mudah dipahami: *Grosir*,
               *Reguler*, dan *Premium* — bukan sekadar "Cluster 0, 1, 2".
            """
        )
        glass_close()

        glass_open()
        st.markdown("##### 🧩 Tiga Fitur Utama Aplikasi")
        st.markdown(
            """
            - **🔮 Prediksi Manual** — masukkan data satu pelanggan lewat form, langsung tahu segmennya.
            - **📁 Upload Massal** — unggah CSV berisi banyak pelanggan sekaligus untuk diberi label segmen.
            - **📊 Dashboard** — jelajahi karakteristik tiap segmen lewat grafik interaktif.
            """
        )
        glass_close()

    with right:
        glass_open()
        st.markdown("##### 🛠️ Dibangun Dengan")
        chips_html = "".join(
            f'<span class="tech-chip">{icon} {name}</span>' for icon, name in TECH_STACK
        )
        st.markdown(chips_html, unsafe_allow_html=True)
        glass_close()

        glass_open()
        st.markdown("##### 🎨 Tiga Segmen Pelanggan")
        for i in range(3):
            meta = CLUSTER_META[i]
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.7rem;">
                    <span style="font-size:1.3rem; color:{meta['color']};">{meta['icon_svg']}</span>
                    <div>
                        <div style="font-family:'Sora',sans-serif; font-weight:700; color:{meta['color']}; font-size:0.92rem;">
                            {meta['short']}
                        </div>
                        <div style="color:#8D96AC; font-size:0.8rem; line-height:1.4;">{meta['desc']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        glass_close()

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # KREDIT PEMBUAT
    # ------------------------------------------------------------------
    st.subheader("👩‍💻 Dibuat Oleh")
    st.caption(
        "Proyek ini dikembangkan sebagai bagian dari eksplorasi penerapan Machine Learning "
        "(K-Means Clustering) untuk kasus segmentasi pelanggan di dunia nyata."
    )

    cred_cols = st.columns(2)
    for col, person in zip(cred_cols, TEAM):
        with col:
            st.markdown(
                f"""
                <div class="team-card">
                    <div class="team-avatar" style="background:{person['color']};">{person['initials']}</div>
                    <div>
                        <p class="team-name">{person['name']}</p>
                        <p class="team-nim">NIM {person['nim']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    if st.button("← Kembali ke Beranda", key="tentang_back", use_container_width=False):
        goto("beranda")
