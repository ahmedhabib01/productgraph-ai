from typing import List, Dict, Any, Set


def detect_new_spec_keys(
    products: List[Dict[str, Any]],
    known_keys: Set[str],
) -> Set[str]:
    current_keys = set()

    for p in products:
        specs = p.get("specs", {})
        if isinstance(specs, dict):
            for k in specs.keys():
                current_keys.add(k)

    return current_keys - known_keys