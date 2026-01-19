import json
from parsing.llm_extract import extract_product_from_datasheet
from ingestion.common import Product
import hashlib


def generate_stable_id(name: str, manufacturer: str) -> str:
    raw = f"{name}|{manufacturer}".lower().strip()
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:8]
    return f"DOC_{h}"

RAW_PATH = "data_sources/_out_raw_datasheets.json"
OUT_PATH = "data_sources/_out_parsed_datasheets_products.json"


def main():
    raw_docs = json.load(open(RAW_PATH, "r", encoding="utf-8"))

    parsed_products = []
    for doc in raw_docs:
        raw_text = doc["raw_text"]
        extracted = extract_product_from_datasheet(raw_text)

        # Wrap into our canonical Product format
        name = str(extracted.get("name", "UNKNOWN"))
        manufacturer = str(extracted.get("manufacturer", "UNKNOWN"))

        pid = extracted.get("id")
        if not pid or str(pid).strip().upper() == "UNKNOWN":
            pid = generate_stable_id(name, manufacturer)

        prod = Product(
            id=str(pid),
            name=name,
            category=str(extracted.get("category", "Unknown")),
            manufacturer=manufacturer,
            specs=extracted.get("specs", {}) if isinstance(extracted.get("specs", {}), dict) else {},
            source="datasheet_llm",
        ).to_dict()


        parsed_products.append(prod)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed_products, f, indent=2)

    print(f"Parsed datasheets into products: {len(parsed_products)}")
    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()