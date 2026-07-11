import pandas as pd
import plotly.express as px
import streamlit as st

from utils.styling import hero, glass_open, glass_close, CLUSTER_META
from utils.model_loader import FEATURES, FEATURE_META, predict_batch


def render():
    hero(
        eyebrow="Langkah 2",
        title="Prediksi Banyak Pelanggan Sekaligus",
        subtitle="Upload file CSV berisi data belanja tahunan banyak pelanggan. Model akan memberi label segmen untuk setiap baris.",
    )
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    glass_open()
    st.markdown("##### 📎 Format CSV yang Dibutuhkan")
    st.write(
        "File CSV wajib memiliki kolom berikut (nama harus persis sama, huruf besar/kecil bebas):"
    )
    cols_preview = st.columns(6)
    for col, feat in zip(cols_preview, FEATURES):
        with col:
            st.markdown(f"**{FEATURE_META[feat]['icon']} `{feat}`**")

    template_df = pd.DataFrame([{f: 0 for f in FEATURES}])
    st.download_button(
        "⬇️ Unduh Template CSV Kosong",
        data=template_df.to_csv(index=False).encode("utf-8"),
        file_name="template_pelanggan.csv",
        mime="text/csv",
    )
    glass_close()

    st.write("")
    uploaded = st.file_uploader("Upload file CSV di sini", type=["csv"])

    if uploaded is not None:
        try:
            raw_df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            st.stop()

        # normalisasi nama kolom biar tidak sensitif kapitalisasi/spasi
        raw_df.columns = [c.strip() for c in raw_df.columns]
        col_map = {c.lower(): c for c in raw_df.columns}
        missing = [f for f in FEATURES if f.lower() not in col_map]

        if missing:
            st.error(
                f"❌ Kolom berikut tidak ditemukan di file kamu: **{', '.join(missing)}**. "
                "Cek kembali nama kolom, atau unduh template di atas sebagai acuan."
            )
            st.stop()

        work_df = raw_df.rename(columns={col_map[f.lower()]: f for f in FEATURES})
        work_df[FEATURES] = work_df[FEATURES].apply(pd.to_numeric, errors="coerce")

        n_invalid = work_df[FEATURES].isna().any(axis=1).sum()
        if n_invalid:
            st.warning(f"⚠️ {n_invalid} baris memiliki nilai kosong/tidak valid dan akan diabaikan.")
            work_df = work_df.dropna(subset=FEATURES)

        if work_df.empty:
            st.error("Tidak ada baris valid untuk diprediksi.")
            st.stop()

        result_df = predict_batch(work_df)

        # tambahkan ke riwayat sesi
        for _, r in result_df.iterrows():
            st.session_state.history.append({**{f: r[f] for f in FEATURES}, "Cluster": int(r["Cluster"]), "Segmen": r["Segmen"], "Sumber": "Upload"})

        st.success(f"✅ Berhasil memprediksi {len(result_df)} pelanggan.")

        # ---------------- Ringkasan ----------------
        m1, m2, m3 = st.columns(3)
        counts = result_df["Segmen"].value_counts()
        for i, col in enumerate([m1, m2, m3]):
            seg_name = CLUSTER_META[i]
            label = seg_name["short"]
            matching = [v for k, v in counts.items() if seg_name["short"] in k]
            val = matching[0] if matching else 0
            with col:
                st.metric(f"{seg_name['icon']} {label}", f"{val} pelanggan")

        st.write("")
        tab1, tab2 = st.tabs(["📋 Tabel Hasil", "📈 Insight Visual"])

        with tab1:
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Unduh Hasil Prediksi (CSV)",
                data=result_df.to_csv(index=False).encode("utf-8"),
                file_name="hasil_segmentasi.csv",
                mime="text/csv",
            )

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                segmen_color_map = {
                    seg_name: CLUSTER_META[i]["color"]
                    for seg_name in result_df["Segmen"].unique()
                    for i in range(3)
                    if CLUSTER_META[i]["short"].lower() in seg_name.lower()
                }
                fig_pie = px.pie(
                    result_df, names="Segmen", hole=0.55,
                    color="Segmen",
                    color_discrete_map=segmen_color_map,
                )
                fig_pie.update_traces(textinfo="percent+label")
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ECEEF6"),
                    showlegend=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=340,
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                st.caption("Distribusi jumlah pelanggan per segmen.")

            with c2:
                feat_pick = st.selectbox("Bandingkan kategori:", FEATURES, index=0)
                fig_box = px.box(result_df, x="Segmen", y=feat_pick, color="Segmen", points="all")
                fig_box.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ECEEF6"),
                    showlegend=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=340,
                )
                st.plotly_chart(fig_box, use_container_width=True)
                st.caption(f"Sebaran nilai {feat_pick} pada masing-masing segmen hasil upload ini.")
    else:
        glass_open()
        st.markdown(
            """
            <div style="text-align:center; padding: 2rem 1rem; color:#8D96AC;">
                <div style="font-size:2.2rem;">📤</div>
                <p>Belum ada file yang diupload. Siapkan CSV dengan format di atas, lalu upload untuk mulai.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        glass_close()
