from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class Product:
    id: str
    name: str
    category: str
    manufacturer: str
    specs: Dict[str, Any]
    source: str  # e.g. "erp_api", "xml", "datasheet"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def safe_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(str(value).strip())
    except Exception:
        return None