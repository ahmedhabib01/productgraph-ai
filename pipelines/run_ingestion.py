import json
from ingestion.from_erp_api import fetch_from_erp_api
from ingestion.from_xml import fetch_from_xml
from ingestion.from_datasheets import fetch_from_datasheets


def main():
    erp = fetch_from_erp_api()
    xml = fetch_from_xml()
    docs = fetch_from_datasheets()

    print(f"ERP products: {len(erp)}")
    print(f"XML products: {len(xml)}")
    print(f"Datasheets: {len(docs)}")

    all_structured = erp + xml

    # Save outputs (this simulates a bronze -> silver step)
    with open("data_sources/_out_structured_products.json", "w", encoding="utf-8") as f:
        json.dump(all_structured, f, indent=2)

    with open("data_sources/_out_raw_datasheets.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

    print("Wrote:")
    print("- data_sources/_out_structured_products.json")
    print("- data_sources/_out_raw_datasheets.json")


if __name__ == "__main__":
    main()