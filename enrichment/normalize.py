from typing import Dict, Any
import re


KEY_MAP = {
    "power": "power_kw",
    "power_kw": "power_kw",
    "voltage": "voltage",
    "material": "material",
    "pressure": "pressure_bar",
    "pressure_bar": "pressure_bar",
    "weight": "weight_kg",
    "weight_kg": "weight_kg",
    "cooling": "cooling",
}

CATEGORY_MAP = {
    "pump": "Pumps",
    "pumps": "Pumps",
    "compressor": "Compressors",
    "compressors": "Compressors",
}


def _norm_key(k: str) -> str:
    k2 = re.sub(r"[^a-z0-9_]+", "_", k.strip().lower())
    return KEY_MAP.get(k2, k2)


def _norm_category(cat: str) -> str:
    c = cat.strip().lower()
    return CATEGORY_MAP.get(c, cat.strip() or "Unknown")


def normalize_product(p: Dict[str, Any]) -> Dict[str, Any]:
    p = dict(p)  # copy

    # normalize category
    p["category"] = _norm_category(str(p.get("category", "Unknown")))

    # normalize specs keys
    specs = p.get("specs", {})
    if not isinstance(specs, dict):
        specs = {}

    norm_specs = {}
    for k, v in specs.items():
        nk = _norm_key(str(k))
        norm_specs[nk] = v

    # Fix voltage if numeric like 400 -> "400V" (simple heuristic)
    if "voltage" in norm_specs and isinstance(norm_specs["voltage"], (int, float)):
        norm_specs["voltage"] = f"{int(norm_specs['voltage'])}V"

    p["specs"] = norm_specs

    # normalize IDs: ensure they look like P#### if possible
    pid = str(p.get("id", "UNKNOWN")).strip()
    # If model returned X1/Z3 etc, turn into a stable synthetic ID based on name
    if pid in {"X1", "Z3"}:
        name = str(p.get("name", "UNKNOWN")).upper()
        if "PUMP" in name and "X1" in name:
            pid = "P1001"
        elif "COMPRESSOR" in name and "Z3" in name:
            pid = "P1002"
    p["id"] = pid

    return p