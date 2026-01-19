import json
from validation.metrics import compute_metrics
from validation.schema_drift import detect_new_spec_keys

DATA_PATH = "data_sources/_out_all_products_normalized.json"

# In a real system this would live in a config / DB
KNOWN_SPEC_KEYS = {
    "power_kw",
    "voltage",
    "material",
    "pressure_bar",
    "weight_kg",
    "cooling",
}


def main():
    products = json.load(open(DATA_PATH, "r", encoding="utf-8"))

    metrics = compute_metrics(products)
    new_keys = detect_new_spec_keys(products, KNOWN_SPEC_KEYS)

    print("📊 Data Quality Metrics")
    for k, v in metrics.items():
        print(f"- {k}: {v}")

    if new_keys:
        print("\nSchema drift detected! New spec keys:")
        for k in sorted(new_keys):
            print(f"- {k}")
    else:
        print("\nNo schema drift detected.")


if __name__ == "__main__":
    main()