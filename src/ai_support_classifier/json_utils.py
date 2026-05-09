from __future__ import annotations

import json
import re
from typing import Any


def strip_json_fences(text: str) -> str:
    """Remove common Markdown JSON fences from model output."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract and parse the first JSON object from a model response."""
    cleaned = strip_json_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(cleaned[start:end + 1])
