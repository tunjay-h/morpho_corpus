# core/lexical_tagger.py
"""
Lexicon-based POS tagger using user-provided dictionary files.
"""
import os
import json
import logging
from typing import Dict, Any

# Base project directory
env_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DICTIONARY_DIR = os.path.join(env_dir, 'dictionaries')


def load_dictionary(lang_code: str = 'az') -> Dict[str, Any]:
    """
    Load word-level dictionary for a given language code.
    Returns the dictionary as a dict. Logs errors if file is missing or corrupt.
    """
    file_path = os.path.join(DICTIONARY_DIR, f"{lang_code}.json")
    if not os.path.exists(file_path):
        logging.error(f"Dictionary '{lang_code}' not found at {file_path}")
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
            logging.info(f"Loaded dictionary for '{lang_code}' with {len(dictionary)} entries.")
            return dictionary
    except Exception as e:
        logging.error(f"Failed to load dictionary '{lang_code}': {e}")
        return {}


def analyze_word_lexical(word: str, lang_code: str = 'az') -> Dict[str, Any]:
    """
    Lookup word in dictionary. Returns:
        {
          'word': original word,
          'POS': part-of-speech tag or 'UNK',
          'features': morphological features dict or empty
        }
    Logs the analysis process.
    """
    dictionary = load_dictionary(lang_code)
    entry = dictionary.get(word.lower()) if dictionary else None
    if entry and isinstance(entry, dict):
        pos = entry.get('POS', 'UNK')
        features = entry.get('Features', {})
        logging.info(f"Lexical analysis for '{word}': POS={pos}, features={features}")
    else:
        pos = 'UNK'
        features = {}
        logging.info(f"Word '{word}' not found in dictionary for '{lang_code}'. Returning UNK.")
    return {'word': word, 'POS': pos, 'features': features}
