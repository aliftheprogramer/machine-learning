# 🌾 Agricultural Prediction ML Service

**Machine Learning Service untuk Analisis Keberhasilan Panen**

Proyek ini adalah layanan backend berbasis Python yang berfungsi untuk memprediksi apakah suatu kegiatan pertanian berhasil mencapai target optimal atau tidak. Layanan ini juga cerdas karena bisa memberikan **"Smart Notes"** (catatan evaluasi) yang menjelaskan *mengapa* hasil panen tersebut bagus atau kurang bagus.

---

## 📚 Daftar Isi
1. [Tentang Proyek](#-tentang-proyek)
2. [Cara Kerja Sistem](#-cara-kerja-sistem)
3. [Data & Model](#-data--model)
4. [Cara Menjalankan](#-cara-menjalankan)
5. [Dokumentasi API](#-dokumentasi-api)

---

## 📖 Tentang Proyek

Dalam pertanian, seringkali petani bingung kenapa hasil panennya sedikit. Apakah karena benihnya jelek? Tanahnya tidak cocok? Atau cara tanamnya salah?

Sistem ini menjawab pertanyaan tersebut dengan:
1.  **Memprediksi Status**: `met` (Sukses/Sesuai Target) atau `not_met` (Gagal/Underperform).
2.  **Memberikan Alasan**: Memberikan teks penjelasan otomatis berdasarkan data input.

---

## ⚙️ Cara Kerja Sistem

Alur kerja proyek ini dibagi menjadi 3 tahap utama:

1.  **Simulasi Data (`train_model.py`)**  
    Karena data riil pertanian sulit didapat, kita membuat "Simulasi Petani Virtual" yang menghasilkan 2000 data dummy. Data ini dibuat mengikuti anturan logika pertanian (agronomi).
    *   *Ingin tahu detail rumus simulasinya? Baca [PENJELASANMENGENAIDATA.md](PENJELASANMENGENAIDATA.md)*.

2.  **Training Model**  
    Data dummy tadi dipelajari oleh algoritma Machine Learning (`RandomForest`). Model belajar pola: "Oh, kalau tanahnya *Grumosol* dan jarak tanamnya *terlalu rapat*, biasanya hasilnya *gagal*."

3.  **Serving API (`app.py`)**  
    Model yang sudah pintar "dibungkus" menjadi API menggunakan Flask. Aplikasi lain (seperti Web/Mobile App) bisa mengirim data ke sini dan mendapat balasan prediksi instan.

---

## 🧠 Data & Model

### 1. Dataset (Synthetic Knowledge Base)
Dataset dibuat otomatis saat Anda menjalankan script training.
-   **Lokasi**: Dibuat di memori dan disimpan juga sebagai `agricultural_data_dummy.csv` untuk Anda lihat.
-   **Fitur Utama**:
    -   `seed_id`: Jenis Benih (Tiap benih punya potensi beda).
    -   `soil_type_id`: Jenis Tanah (Mempengaruhi kesuburan).
    -   `planting_density`: Kepadatan (Jumlah benih dibagi luas lahan).
    -   `yield_ratio`: Efisiensi hasil panen.

### 2. Algoritma ML
-   **Model**: Random Forest Classifier.
-   **Kenapa Random Forest?**: Cocok untuk data tabular dengan banyak aturan "If-Else" yang kompleks (seperti aturan pertanian).
-   **Output**: 
    -   `farm_model_v2.pkl` (Otak model).
    -   `farm_meta.pkl` (Kamus data).

---

## 🚀 Cara Menjalankan

Ikuti langkah ini untuk menjalankan aplikasi di komputer Anda.

### Prasyarat
Pastikan sudah terinstall:
-   Python 3.9 atau lebih baru.
-   Pip (Python Package Manager).

### Langkah 1: Install Library
Buka terminal di folder ini, lalu jalankan:
```bash
pip install -r requirements.txt
```

### Langkah 2: Latih Model (Wajib di Awal!)
Sebelum server bisa jalan, "otak" kecerdasannya harus dibuat dulu.
```bash
python train_model.py
```
*Tanda Berhasil*: Muncul file `farm_model_v2.pkl`, `farm_meta.pkl`, dan `agricultural_data_dummy.csv`.

### Langkah 3: Jalankan Server API
```bash
python app.py
```
Sekarang server siap menerima request di alamat: `http://localhost:5000`

---

## 📡 Dokumentasi API

Anda bisa mengetes API ini menggunakan **Postman**, **cURL**, atau tool testing API lainnya.

### 🔹 Endpoint: Prediksi Panen
**URL**: `POST /predict_harvest`

Gunakan endpoint ini untuk mengirim data laporan panen.

**Contoh Request (JSON Body):**
```json
{
    "seed_id": 1,            // ID Benih (1-7)
    "soil_type_id": 5,       // ID Tanah (1-6). Cth: 5 itu Grumosol (Kurang bagus)
    "land_area": 1000,       // Luas tanah dalam meter persegi
    "plant_qty": 15,         // Jumlah benih ditebar (kg). (Terlalu padat untuk 1000m2!)
    "harvest_qty": 2000      // Hasil panen didapat (kg)
}
```

**Contoh Response Sukses:**
```json
{
    "status": "success",
    "data": {
        "expectation_status": "not_met",
        "notes": "Hasil panen BELUM mencapai target ekspektasi (Underperformance). Jenis tanah Grumosol (Kering/Liat) mungkin menjadi faktor pembatas pertumbuhan akar/air. Indikasi jarak tanam terlalu rapat (Overcrowding) sehingga kompetisi nutrisi tinggi. Realisasi hanya 60% dari potensi genetik benih."
    }
}
```

**Penjelasan Response:**
-   `expectation_status`: **not_met** (Gagal).
-   `notes`: Memberi tahu bahwa tanahnya kurang cocok DAN jarak tanamnya terlalu rapat (Overcrowding). Inilah fitur "Smart Notes".

---

## 🐳 Menjalankan dengan Docker (Opsional)
Jika tidak ingin install Python manual:

1.  **Build Image**:
    ```bash
    docker build -t ml-farm-service .
    ```
2.  **Run Container**:
    ```bash
    docker run -p 5000:5000 ml-farm-service
    ```
