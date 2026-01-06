# Postman Documentation for ML Service

## Base URL
`http://localhost:5000`

## Endpoints

### 1. Predict Harvest
Melakukan prediksi status panen dan menghasilkan smart notes berdasarkan data input.

- **URL**: `/predict_harvest`
- **Method**: `POST`
- **Headers**:
  - `Content-Type`: `application/json`

#### Request Body (JSON)
| Field | Tipe | Deskripsi | Contoh |
|-------|------|-----------|--------|
| `seed_id` | Integer | ID Benih | `1` |
| `soil_type_id` | Integer | ID Tipe Tanah | `1` |
| `land_area` | Number | Luas Lahan (m²) | `1000` |
| `plant_qty` | Number | Jumlah Benih (kg) | `50` |
| `harvest_qty` | Number | Jumlah Panen (kg) | `8000` |

**Contoh Payload (Raw JSON):**
```json
{
    "seed_id": 1,
    "soil_type_id": 1,
    "land_area": 1000,
    "plant_qty": 50,
    "harvest_qty": 8000
}
```

#### Response

**Sukses (200 OK):**
```json
{
    "data": {
        "expectation_status": "met",
        "metrics": {
            "planting_density": "0.0500 kg/m2",
            "soil_factor": "Tanah Aluvial",
            "yield_ratio": "160.0x"
        },
        "notes": "Hasil panen SUKSES mencapai target ekspektasi. Kondisi tanah Tanah Aluvial memberikan kontribusi nutrisi yang sangat baik."
    },
    "status": "success"
}
```

**Error - Data Tidak Lengkap (400 Bad Request):**
```json
{
    "message": "Field wajib belum diisi: harvest_qty",
    "status": "error"
}
```

**Error - Server (500 Internal Server Error):**
```json
{
    "message": "Model not found. Run train_model.py first.",
    "status": "error"
}
```
