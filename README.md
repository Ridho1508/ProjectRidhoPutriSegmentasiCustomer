# 🛍️ Segmentasi Pelanggan — Dashboard Interaktif

Web app Streamlit untuk memprediksi & menjelajahi segmentasi pelanggan grosir
menggunakan model **K-Means** yang sudah kamu latih (`scaler.pkl`, `kmeans_model.pkl`,
`cluster_labels.pkl`). Tema: **dark mode modern / glassmorphism**.

Navigasi aplikasi **tidak memakai sidebar bawaan Streamlit**. Semua menu
(Beranda, Prediksi Manual, Upload Massal, Dashboard, Tentang) ditampilkan sebagai
segmented-control yang bisa langsung dipencet di tengah halaman.

```
customer_segmentation_app/
├── app.py                          # Router utama + menu navigasi tengah
├── views/
│   ├── beranda.py                  # Home: ringkasan model & kartu navigasi
│   ├── prediksi_manual.py          # Input satu pelanggan → prediksi segmen
│   ├── upload_massal.py            # Upload CSV banyak pelanggan sekaligus
│   ├── dashboard.py                # Visualisasi & eksplorasi data
│   └── tentang.py                  # Penjelasan proyek + kredit pembuat
├── utils/
│   ├── model_loader.py             # Load model + fungsi prediksi
│   └── styling.py                  # Tema CSS dark + warna kampus + menu navigasi
├── assets/
│   ├── logo_nusa_putra.png         # Logo asli resolusi tinggi (arsip/keperluan lain)
│   └── logo_nusa_putra_web.png     # Versi dikompres, dipakai app (bar navigasi & watermark)
├── models/
│   ├── scaler.pkl
│   ├── kmeans_model.pkl
│   └── cluster_labels.pkl
├── data/
│   └── sample_data.csv             # Data demo (simulasi) untuk dashboard
├── .streamlit/
│   └── config.toml                 # Tema warna native Streamlit
└── requirements.txt
```

Karena tidak ada folder `pages/`, Streamlit tidak akan membuat navigasi
otomatis di sidebar. Perpindahan antar halaman sepenuhnya diatur lewat
`st.session_state` di `utils/styling.py` (`top_nav()` dan `goto()`), lalu
`app.py` merender view yang sesuai.

---

## 1. Menjalankan di VSCode (lokal)

### a. Buka folder project
Buka VSCode → `File > Open Folder` → pilih folder `customer_segmentation_app`.

### b. Buat virtual environment
Buka terminal di VSCode (`` Ctrl+` ``), lalu jalankan:

```bash
python -m venv venv
```

Aktifkan:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Kalau berhasil, akan muncul `(venv)` di depan prompt terminal. Di pojok kanan
bawah VSCode, pastikan Python Interpreter yang dipakai adalah yang di dalam `venv`
(klik nama interpreter di status bar kalau perlu ganti).

### c. Install dependencies

```bash
pip install -r requirements.txt
```

### d. Jalankan aplikasi

```bash
streamlit run app.py
```

Browser akan otomatis terbuka ke `http://localhost:8501`. Setiap kali kamu
menyimpan perubahan file, cukup klik **"Rerun"** di pojok kanan atas browser
(atau aktifkan **"Always rerun"** supaya auto-refresh).

---

## 2. Cara Kerja Tiap Halaman

| Halaman | Fungsi |
|---|---|
| **Beranda** | Ringkasan model, penjelasan 3 segmen, kartu navigasi ke fitur lain |
| **Prediksi Manual** | Form input 6 kategori belanja → prediksi segmen instan + radar chart posisi pelanggan vs pusat tiap segmen |
| **Upload Massal** | Upload CSV → validasi kolom otomatis → prediksi semua baris → tabel hasil + grafik + tombol download |
| **Dashboard** | Eksplorasi visual: distribusi segmen, profil per kategori (violin/scatter), perbandingan titik pusat cluster. Bisa pakai data demo atau riwayat prediksi sesi kamu sendiri |
| **Tentang** | Penjelasan singkat proyek (masalah, cara kerja model, tech stack) + kredit pembuat |

Riwayat prediksi (dari Prediksi Manual & Upload Massal) disimpan di
`st.session_state`, artinya **hanya bertahan selama tab browser terbuka** —
ini normal untuk Streamlit karena tidak ada database di project ini. Kalau nanti
mau riwayat permanen, tinggal tambahkan koneksi ke database (SQLite/Supabase/dst).

### Format CSV untuk Upload Massal
Kolom wajib (nama harus sama persis, besar-kecil huruf bebas):
`Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen`

Template kosong bisa diunduh langsung dari halaman **Upload Massal**.

---

## 3. Kustomisasi Tampilan

Semua warna & style ada di satu tempat: `utils/styling.py`, di dictionary `COLORS`
dan `CLUSTER_META`. Temanya sekarang dark mode dengan aksen warna khas
**Nusa Putra University** (magenta `#E85D9A` / `#C2185B` & plum `#7E0048`,
diambil langsung dari logo kampus). Contoh ganti salah satu warna aksen:

```python
# di utils/styling.py
COLORS = {
    ...
    "campus_pink": "#E85D9A",   # ganti di sini
    ...
}
```

Semua halaman otomatis ikut berubah karena semuanya memanggil `inject_base_css()`
dan `CLUSTER_META` dari file yang sama — jadi kamu tidak perlu ubah CSS satu-satu.

**Logo kampus** disimpan di `assets/logo_nusa_putra_web.png` (versi terkompres, ~11 KB)
dan otomatis muncul di bar navigasi + sebagai watermark samar di background. File
`assets/logo_nusa_putra.png` (resolusi asli) tetap disimpan sebagai arsip kalau
sewaktu-waktu dibutuhkan untuk keperluan lain (misal cetak/dokumen resmi). Kalau
mau ganti logo, timpa `logo_nusa_putra_web.png` dengan file baru (disarankan
dikompres dulu supaya app tetap ringan).

---

## 3b. Catatan Perbaikan Bug (Navigasi dari Kartu di Beranda)

Sempat ada `StreamlitAPIException` saat tombol "Buka →" di kartu Beranda dipencet.
Penyebabnya: fungsi `goto()` mencoba mengubah `st.session_state["nav_widget"]`
padahal widget menu itu sudah "dipakai" lebih dulu di run yang sama (`top_nav()`
selalu dijalankan sebelum halaman lain dirender) — Streamlit melarang itu.

Sudah diperbaiki: `goto()` sekarang hanya menitipkan halaman tujuan ke
`st.session_state["_pending_nav"]` lalu memanggil `st.rerun()`. Di run
berikutnya, `top_nav()` menerapkan `_pending_nav` ke `nav_widget` **sebelum**
widget-nya dibuat, yang mana diperbolehkan Streamlit. Lihat komentar di
`utils/styling.py` (fungsi `goto()` dan `top_nav()`) untuk detailnya.

---

## 4. Deploy ke Streamlit Community Cloud (gratis)

### a. Upload project ke GitHub
1. Buat repository baru di [github.com](https://github.com) (bisa public atau private).
2. Di terminal VSCode, dari dalam folder project:

```bash
git init
git add .
git commit -m "Initial commit: customer segmentation app"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

> ⚠️ Pastikan folder `venv/` **tidak ikut ter-commit**. Buat file `.gitignore`
> berisi minimal:
> ```
> venv/
> __pycache__/
> *.pyc
> ```

### b. Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io) dan login pakai akun GitHub.
2. Klik **"New app"**.
3. Pilih repository, branch `main`, dan main file path: `app.py`.
4. Klik **Deploy**.

Streamlit Cloud akan otomatis membaca `requirements.txt` untuk install dependencies,
dan `.streamlit/config.toml` untuk tema warna. Setelah proses build selesai (biasanya
1–3 menit), aplikasi kamu sudah online dengan URL publik yang bisa dibagikan.

Setiap kali kamu `git push` perubahan baru ke branch `main`, Streamlit Cloud akan
otomatis rebuild & redeploy — tidak perlu setting ulang.

---

## 5. Troubleshooting Umum

- **`InconsistentVersionWarning` saat load model** → tidak berbahaya, hanya
  peringatan karena versi scikit-learn saat training beda tipis dengan versi
  saat load. Prediksi tetap jalan normal. Kalau ingin hilangkan total, retrain
  & re-pickle model pakai versi scikit-learn yang sama dengan `requirements.txt`.
- **Error "kolom tidak ditemukan" saat upload CSV** → cek nama kolom di file
  kamu harus persis: `Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen`.
- **Ingin menambah halaman baru** → buat file baru di `views/`, tambahkan
  entri baru di dictionary `PAGES` (`utils/styling.py`), lalu daftarkan
  fungsi `render()`-nya di `PAGE_RENDERERS` (`app.py`).

---

## 6. Dibuat Oleh

Proyek ini dikembangkan oleh:
1. **Ridho Safutra** — NIM 20240040121
2. **Putri Prisilia** — NIM 20240040110

Detail lengkap tentang proyek ini juga bisa dilihat langsung di menu
**Tentang** pada aplikasi.

---

Selamat mencoba! 🚀 Kalau mau menambah fitur (misalnya export ke PDF, autentikasi
login, atau riwayat permanen ke database), tinggal lanjut dari struktur yang sudah ada.
