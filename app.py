from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing for all routes

# Load Model & Metadata
try:
    with open('farm_model_v2.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('farm_meta.pkl', 'rb') as f:
        meta = pickle.load(f)
    print("✅ Model & Meta Loaded Successfully")
except:
    print("❌ Model not found. Run train_model.py first.")

def generate_smart_notes(prediction, seed_id, soil_id, density, ratio, std_ratio):
    """
    Fungsi ini merangkai kata-kata (Natural Language Generation sederhana)
    berdasarkan data statistik.
    """
    soil_name = meta['soils'].get(soil_id, "Unknown Soil")
    
    notes = []
    
    # 1. Analisa Status Utama
    if prediction == "met":
        notes.append("Hasil panen SUKSES mencapai target ekspektasi.")
        
        # Puji Tanah jika tanahnya bagus
        if soil_id in [1, 2]:
            notes.append(f"Kondisi tanah {soil_name} memberikan kontribusi nutrisi yang sangat baik.")
        
        # Puji Efisiensi
        if ratio > std_ratio:
            notes.append(f"Produktivitas sangat tinggi ({int(ratio)}x lipat), melebihi standar varietas ({std_ratio}x).")
            
    else: # Not Met
        notes.append("Hasil panen BELUM mencapai target ekspektasi (Underperformance).")
        
        # Analisa Tanah (Blame Soil)
        if soil_id in [4, 5]:
            notes.append(f"Jenis tanah {soil_name} mungkin menjadi faktor pembatas pertumbuhan akar/air.")
        
        # Analisa Kepadatan
        if density > 0.008:
            notes.append("Indikasi jarak tanam terlalu rapat (Overcrowding) sehingga kompetisi nutrisi tinggi.")
        elif density < 0.003:
            notes.append("Populasi tanaman per hektar terlalu sedikit (Jarang), lahan tidak termanfaatkan optimal.")
        
        # Analisa Umum
        pct = (ratio / std_ratio) * 100
        notes.append(f"Realisasi hanya {int(pct)}% dari potensi genetik benih.")

    return " ".join(notes)


@app.route('/predict_harvest', methods=['POST'])
def predict_harvest():
    try:
        data = request.json
        
        # 1. Extract Input
        required_fields = ['seed_id', 'soil_type_id', 'land_area', 'plant_qty', 'harvest_qty']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
             return jsonify({
                "status": "error", 
                "message": f"Field wajib belum diisi: {', '.join(missing_fields)}"
            }), 400

        seed_id = int(data.get('seed_id'))
        soil_id = int(data.get('soil_type_id'))
        land_area = float(data.get('land_area'))    # m2
        plant_qty = float(data.get('plant_qty'))    # kg (benih)
        harvest_qty = float(data.get('harvest_qty')) # kg (panen)
        
        # 2. Feature Engineering (Hitung Variabel Turunan)
        # Hitung Kepadatan (Density)
        planting_density = plant_qty / land_area
        
        # Hitung Rasio Panen (Yield Ratio)
        yield_ratio = harvest_qty / plant_qty
        
        # 3. Prediksi ML
        # Input ke model harus urut sesuai training: [seed_id, soil_type_id, density, yield_ratio]
        prediction_class = model.predict([[seed_id, soil_id, planting_density, yield_ratio]])[0]
        
        # 4. Generate Notes Otomatis
        std_ratio = meta['seeds'].get(seed_id, 200) # Default 200 jika tidak ada
        notes_text = generate_smart_notes(
            prediction_class, seed_id, soil_id, planting_density, yield_ratio, std_ratio
        )
        
        return jsonify({
            "status": "success",
            "data": {
                "expectation_status": prediction_class, # "met" atau "not_met"
                "notes": notes_text,
                "metrics": {
                    "planting_density": f"{planting_density:.4f} kg/m2",
                    "yield_ratio": f"{yield_ratio:.1f}x",
                    "soil_factor": meta['soils'].get(soil_id)
                }
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)