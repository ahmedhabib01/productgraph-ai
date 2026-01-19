from typing import List, Dict, Any
from pathlib import Path

def fetch_from_datasheets(folder: str = "data_sources/pdfs") -> List[Dict[str, Any]]:
    """
    For now we read .txt datasheets (simple + free).
    Next step we'll parse them using a local LLM to extract structured specs.
    """
    out: List[Dict[str, Any]] = []
    for path in Path(folder).glob("*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        out.append(
            {
                "raw_document_id": path.stem,
                "raw_text": text,
                "source": "datasheet_txt",
                "filename": path.name,
            }
        )
    return out