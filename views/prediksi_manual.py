import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.styling import hero, glass_open, glass_close, CLUSTER_META
from utils.model_loader import FEATURES, FEATURE_META, predict_cluster, load_models


def render():
    hero(
        eyebrow="Langkah 1",
        title="Prediksi Segmen Satu Pelanggan",
        subtitle="Masukkan total belanja tahunan pelanggan di tiap kategori, lalu model akan menentukan segmennya secara instan.",
    )
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        glass_open()
        st.markdown("##### 📝 Data Belanja Tahunan")
        with st.form("form_prediksi"):
            input_values = {}
            for feat in FEATURES:
                meta = FEATURE_META[feat]
                input_values[feat] = st.number_input(
                    f"{meta['icon']} {meta['label']}",
                    min_value=0,
                    max_value=meta["max"] * 3,
                    value=int(meta["max"] * 0.15),
                    step=meta["step"],
                    help=f"Total belanja {feat} dalam setahun (unit moneter).",
                )
            submitted = st.form_submit_button("🔮 Prediksi Segmen", use_container_width=True)
        glass_close()

    with right:
        if submitted:
            cluster_id, segmen, distances, scaled_vector = predict_cluster(input_values)
            meta = CLUSTER_META[cluster_id]

            # simpan ke riwayat sesi supaya muncul juga di Dashboard
            record = {**input_values, "Cluster": cluster_id, "Segmen": segmen, "Sumber": "Manual"}
            st.session_state.history.append(record)

            glass_open()
            st.markdown(
                f"""
                <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
                    <div style="font-size:2.6rem; color:{meta['color']};">{meta['icon_svg']}</div>
                    <div style="font-family:'Sora',sans-serif; font-size:1.5rem; font-weight:800; color:{meta['color']};">
                        {segmen}
                    </div>
                    <div style="color:#8D96AC; margin-top:0.3rem;">{meta['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Confidence proxy: makin dekat ke centroid sendiri dibanding centroid lain
            min_dist = distances.min()
            confidence = 1 - (min_dist / distances.sum())
            st.progress(min(max(confidence, 0.0), 1.0), text=f"Keyakinan relatif model: {confidence*100:.0f}%")
            glass_close()

            # Radar chart: profil pelanggan vs rata-rata tiap segmen (dalam skala terstandarisasi)
            scaler, kmeans, cluster_labels = load_models()

            def hex_to_rgba(hex_color, alpha=0.2):
                hex_color = hex_color.lstrip("#")
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                return f"rgba({r},{g},{b},{alpha})"

            categories = FEATURES + [FEATURES[0]]
            fig = go.Figure()

            colors_order = [CLUSTER_META[i]["color"] for i in range(kmeans.n_clusters)]
            for i in range(kmeans.n_clusters):
                center_vals = list(kmeans.cluster_centers_[i]) + [kmeans.cluster_centers_[i][0]]
                fig.add_trace(go.Scatterpolar(
                    r=center_vals,
                    theta=categories,
                    name=cluster_labels[i],
                    line=dict(color=colors_order[i], width=1.5, dash="dot"),
                    opacity=0.55,
                ))

            cust_vals = list(scaled_vector) + [scaled_vector[0]]
            fig.add_trace(go.Scatterpolar(
                r=cust_vals,
                theta=categories,
                name="Pelanggan Ini",
                fill="toself",
                line=dict(color=meta["color"], width=3),
                fillcolor=hex_to_rgba(meta["color"], 0.2),
            ))

            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(255,255,255,0.02)",
                    radialaxis=dict(color="#8D96AC", gridcolor="rgba(255,255,255,0.08)"),
                    angularaxis=dict(color="#ECEEF6", gridcolor="rgba(255,255,255,0.08)"),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ECEEF6", family="Inter"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15),
                margin=dict(t=30, b=10, l=30, r=30),
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Grafik menunjukkan posisi pelanggan (area terisi) dibanding pusat tiap segmen, dalam skala terstandarisasi.")
        else:
            glass_open()
            st.markdown(
                """
                <div style="text-align:center; padding: 2.5rem 1rem; color:#8D96AC;">
                    <div style="font-size:2.2rem;">👈</div>
                    <p>Isi form di sebelah kiri lalu klik <b>Prediksi Segmen</b> untuk melihat hasilnya di sini.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            glass_close()

    if st.session_state.history:
        st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
        st.markdown("##### 🕘 Riwayat Prediksi (sesi ini)")
        hist_df = pd.DataFrame(st.session_state.history)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
