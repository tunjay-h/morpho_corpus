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

def load_corpus() -> List[Dict[str, Any]]:
    """
    Load the entire annotated corpus.
    """
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_corpus(corpus: List[Dict[str, Any]]) -> None:
    """
    Save the annotated corpus to disk.
    """
    os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
    with open(CORPUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

def add_entry(text: str, tokens: List[Dict[str, Any]]) -> None:
    """
    Add a new annotated sentence to the corpus.
    """
    corpus = load_corpus()
    corpus.append({'text': text, 'tokens': tokens})
    save_corpus(corpus)

def get_corpus() -> List[Dict[str, Any]]:
    """
    Retrieve the annotated corpus.
    """
    return load_corpus()
