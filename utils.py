import json
from typing import Dict, Any


def safe_json_parse(text: str) -> Dict[str, Any]:
    """Safely parse JSON from text response."""
    start = text.find('{')
    end = text.rfind('}') + 1
    if start != -1 and end != 0:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            return {"solutions": [text]} if "solutions" in text else {"review": text}
    return {"solutions": [text]} if "solutions" in text else {"review": text}