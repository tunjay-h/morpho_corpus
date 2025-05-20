# db/corpus.py
"""
Corpus database storage and retrieval.
"""

import os
import json
from typing import List, Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CORPUS_DIR = os.path.join(BASE_DIR, 'corpus')
CORPUS_PATH = os.path.join(CORPUS_DIR, 'corpus.json')

import logging

def load_corpus() -> List[Dict[str, Any]]:
    """
    Load the entire annotated corpus from disk.
    Logs the number of entries loaded or errors.
    """
    if not os.path.exists(CORPUS_PATH):
        logging.warning(f"Corpus file not found at {CORPUS_PATH}")
        return []
    try:
        with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
            logging.info(f"Loaded corpus with {len(corpus)} entries.")
            return corpus
    except Exception as e:
        logging.error(f"Failed to load corpus: {e}")
        return []

def save_corpus(corpus: List[Dict[str, Any]]) -> None:
    """
    Save the annotated corpus to disk. Logs success or errors.
    """
    try:
        os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
        with open(CORPUS_PATH, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)
        logging.info(f"Saved corpus with {len(corpus)} entries to {CORPUS_PATH}")
    except Exception as e:
        logging.error(f"Failed to save corpus: {e}")

def add_entry(text: str, tokens: List[Dict[str, Any]]) -> None:
    """
    Add a new annotated sentence to the corpus. Logs the operation.
    """
    corpus = load_corpus()
    corpus.append({'text': text, 'tokens': tokens})
    save_corpus(corpus)
    logging.info(f"Added entry: '{text[:40]}...' with {len(tokens)} tokens.")

def get_corpus() -> List[Dict[str, Any]]:
    """
    Retrieve the annotated corpus. (Alias for load_corpus)
    """
    return load_corpus()
