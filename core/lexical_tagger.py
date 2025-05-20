# core/lexical_tagger.py
"""
Lexicon-based POS tagger using user-provided dictionary files.
"""
import os
import json
from typing import Dict, Any

# Base project directory
env_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DICTIONARY_DIR = os.path.join(env_dir, 'dictionaries')


def load_dictionary(lang_code: str = 'az') -> Dict[str, Any]:
    """
    Load word-level dictionary for a given language code.
    Raises FileNotFoundError if the JSON file is missing.
    """
    file_path = os.path.join(DICTIONARY_DIR, f"{lang_code}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dictionary '{lang_code}' not found at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_word_lexical(word: str, lang_code: str = 'az') -> Dict[str, Any]:
    """
    Lookup word in dictionary. Returns:
    {
      'word': original word,
      'POS': part-of-speech tag or 'UNK',
      'features': morphological features dict or empty
    }
    """
    dictionary = load_dictionary(lang_code)
    entry = dictionary.get(word.lower())
    if entry and isinstance(entry, dict):
        pos = entry.get('POS', 'UNK')
        features = entry.get('Features', {})
    else:
        pos = 'UNK'
        features = {}

    return {'word': word, 'POS': pos, 'features': features}
