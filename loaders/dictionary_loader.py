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

import logging

def _load_json(path: str) -> Dict[str, Any]:
    """
    Load JSON file from given path. Logs success or errors.
    """
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"Loaded JSON from {path} ({len(data)} entries)")
            return data
    except Exception as e:
        logging.error(f"Failed to load JSON from {path}: {e}")
        return {}

def load_roots() -> Dict[str, Dict[str, Any]]:
    """
    Load root lexicon. Logs operation.
    """
    return _load_json(ROOTS_PATH)

def load_affixes() -> Dict[str, Dict[str, Any]]:
    """
    Load affix lexicon. Logs operation.
    """
    return _load_json(AFFIXES_PATH)

def load_rules() -> Dict[str, Any]:
    """
    Load morphological rules. Logs operation.
    """
    return _load_json(RULES_PATH)
