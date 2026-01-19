import json
from enrichment.normalize import normalize_product

IN_STRUCTURED = "data_sources/_out_structured_products.json"
IN_PARSED = "data_sources/_out_parsed_datasheets_products.json"
OUT_ALL = "data_sources/_out_all_products_normalized.json"


def main():
    structured = json.load(open(IN_STRUCTURED, "r", encoding="utf-8"))
    parsed = json.load(open(IN_PARSED, "r", encoding="utf-8"))

    combined = structured + parsed
    normalized = [normalize_product(p) for p in combined]

    with open(OUT_ALL, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2)

    print(f"Combined products: {len(combined)}")
    print(f"Normalized products: {len(normalized)}")
    print(f"Wrote: {OUT_ALL}")


if __name__ == "__main__":
    main()