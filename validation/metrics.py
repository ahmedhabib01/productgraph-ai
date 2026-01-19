from typing import List, Dict, Any
from collections import Counter


def compute_metrics(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(products)

    missing_manufacturer = sum(
        1 for p in products if not str(p.get("manufacturer", "")).strip()
    )
    missing_category = sum(
        1 for p in products if not str(p.get("category", "")).strip()
    )
    empty_specs = sum(
        1 for p in products if not isinstance(p.get("specs", {}), dict) or len(p["specs"]) == 0
    )

    sources = Counter(p.get("source", "unknown") for p in products)

    return {
        "total_products": total,
        "missing_manufacturer": missing_manufacturer,
        "missing_category": missing_category,
        "empty_specs": empty_specs,
        "by_source": dict(sources),
    }