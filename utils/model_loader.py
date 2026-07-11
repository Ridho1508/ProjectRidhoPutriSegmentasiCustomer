"""
model_loader.py
-----------------
Semua hal yang berkaitan dengan model (load pickle, prediksi) dikumpulkan di sini.
Kalau nanti kamu ganti model / retrain, file inilah yang perlu disentuh.
"""

import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")  # meredam warning versi sklearn saat unpickle

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

# Metadata fitur: dipakai untuk label input, ikon, dan batas slider yang masuk akal
FEATURE_META = {
    "Fresh": {"icon": "🥬", "label": "Fresh (produk segar)", "max": 120000, "step": 500},
    "Milk": {"icon": "🥛", "label": "Milk (susu & olahan)", "max": 80000, "step": 500},
    "Grocery": {"icon": "🛒", "label": "Grocery (kebutuhan grosir)", "max": 100000, "step": 500},
    "Frozen": {"icon": "🧊", "label": "Frozen (produk beku)", "max": 60000, "step": 500},
    "Detergents_Paper": {"icon": "🧴", "label": "Detergents & Paper", "max": 40000, "step": 250},
    "Delicassen": {"icon": "🍱", "label": "Delicassen (makanan siap saji)", "max": 50000, "step": 250},
}

FEATURES = list(FEATURE_META.keys())


@st.cache_resource(show_spinner=False)
def load_models():
    """Load scaler, kmeans model, dan mapping label cluster. Di-cache supaya cuma dibaca sekali."""
    with open(MODELS_DIR / "scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open(MODELS_DIR / "kmeans_model.pkl", "rb") as f:
        kmeans = pickle.load(f)
    with open(MODELS_DIR / "cluster_labels.pkl", "rb") as f:
        cluster_labels = pickle.load(f)
    return scaler, kmeans, cluster_labels


def predict_cluster(input_dict: dict):
    """
    Terima dict {nama_fitur: nilai}, kembalikan (cluster_id, nama_segmen, jarak_ke_tiap_pusat_cluster).
    """
    scaler, kmeans, cluster_labels = load_models()
    row = pd.DataFrame([[input_dict[f] for f in FEATURES]], columns=FEATURES)
    scaled = scaler.transform(row)
    cluster_id = int(kmeans.predict(scaled)[0])
    distances = kmeans.transform(scaled)[0]  # jarak ke tiap centroid, makin kecil makin dekat
    return cluster_id, cluster_labels[cluster_id], distances, scaled[0]


def predict_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Terima DataFrame dengan kolom sesuai FEATURES, kembalikan DataFrame + kolom Cluster & Segmen."""
    scaler, kmeans, cluster_labels = load_models()
    scaled = scaler.transform(df[FEATURES])
    cluster_ids = kmeans.predict(scaled)
    out = df.copy()
    out["Cluster"] = cluster_ids
    out["Segmen"] = [cluster_labels[c] for c in cluster_ids]
    return out


def get_cluster_centers_original_scale() -> pd.DataFrame:
    """Kembalikan titik pusat tiap cluster dalam skala asli (bukan hasil standardisasi), untuk dibandingkan."""
    scaler, kmeans, cluster_labels = load_models()
    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    df = pd.DataFrame(centers_original, columns=FEATURES)
    df.insert(0, "Segmen", [cluster_labels[i] for i in range(len(df))])
    df.insert(0, "Cluster", range(len(df)))
    return df
