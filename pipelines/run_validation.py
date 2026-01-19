import json
from validation.checks import validate_products

PATH = "data_sources/_out_all_products_normalized.json"


def main():
    products = json.load(open(PATH, "r", encoding="utf-8"))
    ok, errors = validate_products(products)

    if ok:
        print("✅ Validation passed. No issues found.")
        return

    print("❌ Validation failed. Issues:")
    for e in errors[:50]:
        print("-", e)

    # Make the pipeline fail in CI / real runs
    raise SystemExit(1)


if __name__ == "__main__":
    main()