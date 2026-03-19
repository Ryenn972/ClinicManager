from __future__ import annotations
import json
import os
from typing import Dict, Any

def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"patients": {}, "consultations": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"patients": {}, "consultations": {}}
        data.setdefault("patients", {})
        data.setdefault("consultations", {})
        return data
    except json.JSONDecodeError:
        # Fichier corrompu: on repart d'une base vide
        return {"patients": {}, "consultations": {}}

def save_json(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
