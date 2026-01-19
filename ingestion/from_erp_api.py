from typing import List, Dict, Any
import requests
from ingestion.common import Product

ERP_URL = "http://127.0.0.1:8000/products"


def fetch_from_erp_api() -> List[Dict[str, Any]]:
    resp = requests.get(ERP_URL, timeout=10)
    resp.raise_for_status()

    products = []
    for p in resp.json():
        products.append(
            Product(
                id=p["id"],
                name=p["name"],
                category=p.get("category", "Unknown"),
                manufacturer=p.get("manufacturer", "Unknown"),
                specs=p.get("specs", {}),
                source="erp_api",
            ).to_dict()
        )
    return products