from typing import List, Dict, Any, Tuple


REQUIRED_FIELDS = ["id", "name", "category", "manufacturer", "specs", "source"]


def validate_products(products: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    errors = []

    for i, p in enumerate(products):
        for f in REQUIRED_FIELDS:
            if f not in p:
                errors.append(f"[row {i}] missing field: {f}")

        if not isinstance(p.get("specs", {}), dict):
            errors.append(f"[row {i}] specs is not a dict")

        if str(p.get("id", "")).strip() in {"", "UNKNOWN"}:
            errors.append(f"[row {i}] id is empty/UNKNOWN")

        if str(p.get("name", "")).strip() in {"", "UNKNOWN"}:
            errors.append(f"[row {i}] name is empty/UNKNOWN")

    ok = len(errors) == 0
    return ok, errors