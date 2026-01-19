from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from ingestion.common import Product, safe_float


def fetch_from_xml(path: str = "data_sources/xml/products.xml") -> List[Dict[str, Any]]:
    tree = ET.parse(path)
    root = tree.getroot()

    products: List[Dict[str, Any]] = []
    for node in root.findall("product"):
        pid = node.findtext("id") or "UNKNOWN"
        name = node.findtext("name") or "UNKNOWN"
        category = node.findtext("category") or "Unknown"
        manufacturer = node.findtext("manufacturer") or "Unknown"

        # Grab possible specs (simple + flexible)
        specs = {}
        for tag in ["power_kw", "material", "pressure_bar", "cooling", "weight_kg", "voltage"]:
            val = node.findtext(tag)
            if val is None:
                continue
            # try numeric conversion where it makes sense
            if tag in {"power_kw", "pressure_bar", "weight_kg"}:
                num = safe_float(val)
                specs[tag] = num if num is not None else val
            else:
                specs[tag] = val

        products.append(
            Product(
                id=pid,
                name=name,
                category=category,
                manufacturer=manufacturer,
                specs=specs,
                source="xml",
            ).to_dict()
        )

    return products