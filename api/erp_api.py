from fastapi import FastAPI

app = FastAPI()

# Fake ERP product database
PRODUCTS = [
    {
        "id": "P1001",
        "name": "Industrial Water Pump X1",
        "category": "Pumps",
        "manufacturer": "AquaTech",
        "specs": {
            "power_kw": 5.5,
            "voltage": "400V",
            "material": "Stainless Steel"
        }
    },
    {
        "id": "P1002",
        "name": "Hydraulic Compressor Z3",
        "category": "Compressors",
        "manufacturer": "HydroWorks",
        "specs": {
            "pressure_bar": 250,
            "weight_kg": 120,
            "cooling": "Air"
        }
    }
]

@app.get("/products")
def get_products():
    return PRODUCTS