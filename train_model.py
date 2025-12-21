import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# 1. SIMULASI DATA LATIHAN (KNOWLEDGE BASE)
# ==========================================
# Kita buat 1000 data dummy yang mengikuti pola pertanian logis
data_dummy = []

# Referensi Standar Benih (Output per 1 kg)
seed_std = {
    1: 350, 2: 250, 3: 200, 4: 180, 5: 500, 6: 400, 7: 80
}

# Referensi Kualitas Tanah (Modifier)
# Andosol (2) & Aluvial (1) sangat bagus (x1.2), Grumosol (5) jelek (x0.8)
soil_quality = {
    1: 1.1, 2: 1.3, 3: 1.0, 4: 0.9, 5: 0.7, 6: 0.9
}

print("Sedang men-generate data simulasi pertanian...")

for _ in range(2000): # Buat 2000 baris data sejarah
    # A. Acak Faktor Input
    seed_id = np.random.randint(1, 8)       # ID 1-7
    soil_id = np.random.randint(1, 7)       # ID 1-6
    land_area = np.random.randint(500, 5000) # 500m2 - 5000m2
    
    # B. Hitung Kebutuhan Benih Wajar (Misal 1kg utk 200m2)
    ideal_qty = land_area / 200 
    # Variasikan input benih (kadang petani tanam terlalu rapat/jarang)
    plant_qty = ideal_qty * np.random.uniform(0.8, 1.5) 
    
    # C. Hitung Density (Kepadatan)
    planting_density = plant_qty / land_area # kg per m2

    # D. Hitung Potensi Hasil (Rumus Simulasi Alam)
    base_yield = plant_qty * seed_std[seed_id]
    
    # Modifier Tanah
    soil_factor = soil_quality[soil_id]
    
    # Modifier Density (Kalau terlalu padat, hasil turun)
    density_factor = 1.0
    if planting_density > 0.008: # Terlalu padat
        density_factor = 0.7
    elif planting_density < 0.003: # Terlalu jarang
        density_factor = 0.8
        
    # E. HASIL AKHIR (Randomized noise cuaca dll)
    real_yield = base_yield * soil_factor * density_factor * np.random.uniform(0.7, 1.1)
    
    # F. TENTUKAN LABEL (Met / Not Met)
    # Target kita adalah standar benih dasar. 
    # Jika hasil > 85% dari standar benih murni, kita anggap "met"
    target_threshold = plant_qty * seed_std[seed_id] * 0.85
    
    status = "met" if real_yield >= target_threshold else "not_met"

    data_dummy.append({
        "seed_id": seed_id,
        "soil_type_id": soil_id,
        "planting_density": planting_density,
        "yield_ratio": real_yield / plant_qty, # Rasio hasil per kg benih
        "status": status
    })

df = pd.DataFrame(data_dummy)

# ==========================================
# 2. TRAINING RANDOM FOREST
# ==========================================
# Features (X): seed_id, soil_type_id, planting_density, yield_ratio
# Target (y): status
X = df[['seed_id', 'soil_type_id', 'planting_density', 'yield_ratio']]
y = df['status']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ==========================================
# 3. SIMPAN MODEL
# ==========================================
with open('farm_model_v2.pkl', 'wb') as f:
    pickle.dump(model, f)

# Simpan metadata untuk referensi text generation
meta_data = {
    "seeds": seed_std,
    "soils": {
        1: "Aluvial (Subur)", 2: "Andosol (Sangat Subur)", 3: "Latosol (Cukup)",
        4: "Regosol (Pasir/Kasar)", 5: "Grumosol (Kering/Liat)", 6: "Podsolik (Asam)"
    }
}
with open('farm_meta.pkl', 'wb') as f:
    pickle.dump(meta_data, f)

print("✅ Model Random Forest berhasil dilatih dengan faktor Tanah & Kepadatan!")