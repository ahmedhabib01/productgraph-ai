import json
import re
from typing import Dict, Any, Optional
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:3b"


def _extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """
    Ollama sometimes returns extra text.
    This tries to find the first {...} JSON object in the response safely.
    """
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    candidate = match.group(0)
    try:
        return json.loads(candidate)
    except Exception:
        return None


def extract_product_from_datasheet(raw_text: str) -> Dict[str, Any]:
    prompt = f"""
You are a data extraction system for industrial product datasheets.

Extract a SINGLE product as strict JSON with exactly these keys:
- id (string, if missing use "UNKNOWN")
- name (string)
- category (string, guess one word like Pumps/Compressors/Valves)
- manufacturer (string, if missing use "UNKNOWN")
- specs (object/dict with key-value pairs; numbers should be numbers when possible)

Return ONLY JSON. No extra text.

DATASHEET:
{raw_text}
""".strip()

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()

    # Ollama returns the model output in the "response" field
    response_text = data.get("response", "").strip()

    parsed = _extract_first_json_object(response_text)
    if parsed is None:
        # fallback if model didn't behave
        parsed = {
            "id": "UNKNOWN",
            "name": "UNKNOWN",
            "category": "Unknown",
            "manufacturer": "UNKNOWN",
            "specs": {"raw_text": raw_text[:500]},
        }

    return parsed