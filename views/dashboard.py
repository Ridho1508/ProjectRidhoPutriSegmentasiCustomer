from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.styling import hero, CLUSTER_META
from utils.model_loader import FEATURES, get_cluster_centers_original_scale

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_data.csv"


def render():
    hero(
        eyebrow="Langkah 3",
        title="Dashboard Karakteristik Segmen",
        subtitle="Eksplorasi pola belanja tiap segmen memakai data demo, ditambah riwayat prediksi yang sudah kamu buat di sesi ini.",
    )
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    source = st.radio(
        "Sumber data yang ditampilkan:",
        ["🧪 Data Demo (simulasi)", "🕘 Riwayat Prediksi Sesi Ini"],
        horizontal=True,
    )

    if source.startswith("🧪"):
        df = pd.read_csv(DATA_PATH)
        st.caption(
            "Data ini **disimulasikan** berdasarkan pusat cluster model (bukan data pelanggan asli), "
            "khusus untuk demo eksplorasi dashboard."
        )
    else:
        if not st.session_state.history:
            st.info("Belum ada riwayat prediksi di sesi ini. Coba buka menu **Prediksi Manual** atau **Upload Massal** dulu.")
            st.stop()
        df = pd.DataFrame(st.session_state.history)

    segmen_color_map = {
        seg_name: CLUSTER_META[i]["color"]
        for seg_name in df["Segmen"].unique()
        for i in range(3)
        if CLUSTER_META[i]["short"].lower() in seg_name.lower()
    }

    # ------------------------------------------------------------------
    # METRIC RINGKAS
    # ------------------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Pelanggan", len(df))
    with m2:
        dominant = df["Segmen"].value_counts().idxmax()
        st.metric("Segmen Terbesar", dominant)
    with m3:
        st.metric("Rata-rata Fresh", f"{df['Fresh'].mean():,.0f}")
    with m4:
        st.metric("Rata-rata Grocery", f"{df['Grocery'].mean():,.0f}")

    st.write("")

    tab1, tab2, tab3 = st.tabs(["📦 Distribusi Segmen", "🔬 Profil per Kategori", "🧭 Perbandingan Pusat Cluster"])

    with tab1:
        c1, c2 = st.columns([1, 1.3])
        with c1:
            fig = px.pie(df, names="Segmen", hole=0.55, color="Segmen", color_discrete_map=segmen_color_map)
            fig.update_traces(textinfo="percent+label")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#ECEEF6"),
                showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=360,
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            counts = df["Segmen"].value_counts().reset_index()
            counts.columns = ["Segmen", "Jumlah"]
            fig_bar = px.bar(counts, x="Segmen", y="Jumlah", color="Segmen", color_discrete_map=segmen_color_map, text="Jumlah")
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ECEEF6"), showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10), height=360,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        feat_pick = st.selectbox("Pilih kategori produk:", FEATURES, index=0, key="dash_feat")
        fig_violin = px.violin(
            df, x="Segmen", y=feat_pick, color="Segmen", box=True, points="all",
            color_discrete_map=segmen_color_map,
        )
        fig_violin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECEEF6"), showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10), height=420,
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        st.caption(f"Sebaran nilai {feat_pick} pada masing-masing segmen — makin lebar bentuknya, makin bervariasi.")

        st.write("")
        x_feat = st.selectbox("Sumbu X:", FEATURES, index=1, key="dash_x")
        y_feat = st.selectbox("Sumbu Y:", FEATURES, index=2, key="dash_y")
        fig_scatter = px.scatter(
            df, x=x_feat, y=y_feat, color="Segmen", color_discrete_map=segmen_color_map,
            opacity=0.75, size_max=10,
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECEEF6"),
            margin=dict(t=10, b=10, l=10, r=10), height=420,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        centers_df = get_cluster_centers_original_scale()
        st.markdown("##### Titik Pusat (rata-rata) Tiap Segmen — Skala Asli")
        st.dataframe(centers_df, use_container_width=True, hide_index=True)

        melted = centers_df.melt(id_vars=["Cluster", "Segmen"], value_vars=FEATURES, var_name="Kategori", value_name="Nilai")
        fig_radar_bar = px.bar(
            melted, x="Kategori", y="Nilai", color="Segmen", barmode="group",
            color_discrete_map=segmen_color_map,
        )
        fig_radar_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECEEF6"),
            margin=dict(t=10, b=10, l=10, r=10), height=420,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_radar_bar, use_container_width=True)
        st.caption("Ini menunjukkan rata-rata belanja tiap kategori untuk masing-masing segmen — sumber kebenaran dari model K-Means.")
