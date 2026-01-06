# Alur Terjadinya Data Dummy (Simulasi Pertanian)

Data dummy ini dibuat melalui proses **simulasi** di dalam file `train_model.py`. Kita tidak menggunakan data dari lapangan, melainkan membuat "dunia virtual" di mana 2000 petani sedang bercocok tanam.

Berikut adalah langkah-langkah logis bagaimana setiap baris data tercipta:

## 1. Menentukan Aturan Main (Knowledge Base)
Sebelum simulasi dimulai, kita menetapkan aturan dasar agronomi dalam bentuk kamus (dictionary):
- Setiap **ID Benih** punya standar hasil panen per kg.
- Setiap **ID Tanah** punya faktor pengali (subur atau tidak).

```python
# Referensi Standar Benih (Output per 1 kg)
seed_std = {
    1: 350, 2: 250, 3: 200, 4: 180, 5: 500, 6: 400, 7: 80
}

# Referensi Kualitas Tanah (Modifier)
# Contoh: ID 2 (Andosol) dikali 1.3 (sangat subur), ID 5 (Grumosol) dikali 0.7 (jelek)
soil_quality = {
    1: 1.1, 2: 1.3, 3: 1.0, 4: 0.9, 5: 0.7, 6: 0.9
}
```

## 2. Simulasi Per Petani (Looping)
Kita melakukan perulangan sebanyak 2000 kali. Setiap satu putaran loop mewakili satu kejadian tanam seorang petani.

```python
for _ in range(2000):
```

### Langkah A: Mengacak Kondisi Awal
Komputer mengacak situasi lapangan menggunakan fungsi random: jenis benih, jenis tanah, dan luas lahan.

```python
seed_id = np.random.randint(1, 8)       # Pilih benih acak (ID 1-7)
soil_id = np.random.randint(1, 7)       # Pilih tanah acak (ID 1-6)
land_area = np.random.randint(500, 5000) # Luas lahan acak antara 500-5000 m2
```

### Langkah B: Perilaku Petani (Menebar Benih)
Disini kita mensimulasikan "human error". Petani tidak selalu menebar benih dengan jumlah pas.
- **Ideal**: 1kg benih untuk 200m2.
- **Realita**: Kita kalikan faktor acak `0.8` (irit) s/d `1.5` (boros/padat).

```python
ideal_qty = land_area / 200 
plant_qty = ideal_qty * np.random.uniform(0.8, 1.5) 
```

### Langkah C: Hitung Kepadatan (Density)
Kepadatan = Jumlah Benih / Luas Lahan. Ini adalah variabel fisika penting untuk menentukan apakah tanaman berebut nutrisi.

```python
planting_density = plant_qty / land_area
```

### Langkah D: Proses Alam (Menghitung Hasil Panen)
Ini adalah inti simulasinya. Kita menghitung hasil panen (`real_yield`) berdasarkan rumus perkalian faktor:
> `Hasil = Potensi Benih x Faktor Tanah x Faktor Kepadatan x Faktor Cuaca`

1. **Potensi Dasar**: Jumlah benih dikali standar kekuatan benih.
2. **Efek Tanah**: Dikali multiplier tanah (tanah bagus hasil naik).
3. **Efek Kepadatan**: 
    - Jika terlalu padat (`> 0.008`) hasil didiskon 30% (`x 0.7`). 
    - Jika terlalu jarang (`< 0.003`) hasil didiskon 20% (`x 0.8`).
4. **Faktor Cuaca/Noise**: Dikali angka acak 0.7 - 1.1 (unsur ketidakpastian alam).

```python
# Hitung Potensi Dasar
base_yield = plant_qty * seed_std[seed_id]

# Cek Kepadatan (Density Factor)
density_factor = 1.0
if planting_density > 0.008: 
    density_factor = 0.7 # Hukuman terlalu padat
elif planting_density < 0.003: 
    density_factor = 0.8 # Hukuman terlalu jarang

# Hasil Akhir (Real Yield)
# soil_factor didapat dari dictionary soil_quality[soil_id]
real_yield = base_yield * soil_factor * density_factor * np.random.uniform(0.7, 1.1)
```

### Langkah E: Penilaian (Labeling)
Terakhir, komputer menjadi "juri". Apakah hasil panen ini dianggap **sukses (met)** atau **gagal (not_met)**?
Targetnya adalah 85% dari potensi murni benih. Jika di atas itu, dianggap sukses.

```python
target_threshold = plant_qty * seed_std[seed_id] * 0.85

status = "met" if real_yield >= target_threshold else "not_met"
```

## 3. Training
Data-data hasil hitungan di atas (`seed_id`, `soil_id`, `planting_density`, `yield_ratio`, `status`) dikumpulkan menjadi tabel (DataFrame) dan dijadikan bahan belajar untuk model Machine Learning.
