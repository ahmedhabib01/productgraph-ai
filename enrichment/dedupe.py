import re
from typing import List, Dict, Any, Tuple


def _tokens(s: str) -> set:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return set(t for t in s.split() if t)


def similarity(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union


def find_duplicate_pairs(products: List[Dict[str, Any]], threshold: float = 0.6) -> List[Tuple[str, str, float]]:
    """
    Returns pairs (id1, id2, score) that look like duplicates.
    Only compares products with the same manufacturer.
    """
    pairs = []
    n = len(products)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = products[i], products[j]
            if str(p1.get("manufacturer", "")).strip().lower() != str(p2.get("manufacturer", "")).strip().lower():
                continue
            # never mark a product as duplicate of itself
            if str(p1.get("id")) == str(p2.get("id")):
                continue

            s = similarity(str(p1.get("name", "")), str(p2.get("name", "")))
            
            if s >= threshold:
                pairs.append((p1["id"], p2["id"], s))
    return pairs