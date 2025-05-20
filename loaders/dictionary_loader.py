# dictionary_loader.py
"""
Load Azerbaijani lexicons for roots, affixes, and rules.
"""
import json
import os
from typing import Any, Dict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
ROOTS_PATH = os.path.join(BASE_DIR, 'roots.json')
AFFIXES_PATH = os.path.join(BASE_DIR, 'affixes.json')
RULES_PATH = os.path.join(BASE_DIR, 'rules.json')

def _load_json(path: str) -> Dict[str, Any]:
    """Load JSON file from given path."""
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_roots() -> Dict[str, Dict[str, Any]]:
    """Load root lexicon."""
    return _load_json(ROOTS_PATH)

def load_affixes() -> Dict[str, Dict[str, Any]]:
    """Load affix lexicon."""
    return _load_json(AFFIXES_PATH)

def load_rules() -> Dict[str, Any]:
    """Load morphological rules."""
    return _load_json(RULES_PATH)
