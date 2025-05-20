# core/engine.py
"""
Rule-based morphological engine for Azerbaijani.
"""
from typing import List, Dict
from loaders.dictionary_loader import load_roots, load_affixes, load_rules
from core.lexical_tagger import analyze_word_lexical
from core.fst_engine import FSTEngine
from core.gnn_disambiguator import GNNDisambiguator
import os, json

import logging
fst_path = os.path.join(os.path.dirname(__file__), '..', 'fst', 'az.hfst')
if os.path.exists(fst_path):
    print(f"[INFO] Using compiled FST: {fst_path}")
    fst_engine = FSTEngine(fst_bin_path=fst_path)
else:
    print("[INFO] Compiled FST not found, using simulated FST engine.")
    fst_engine = FSTEngine(fst_bin_path=None)
# Load tag vocab for GNNDisambiguator (assume it's at data/tag_vocab.json)
tag_vocab_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tag_vocab.json')
if os.path.exists(tag_vocab_path):
    with open(tag_vocab_path, encoding='utf-8') as f:
        tag_vocab = json.load(f)
    gnn_disamb = GNNDisambiguator(tag_vocab)
else:
    gnn_disamb = None


def analyze_word(word: str) -> List[Dict]:
    """Perform FST-based morphological analysis of a single word, use GNN for disambiguation, fallback to lexical if needed."""
    fst_results = fst_engine.analyze(word)
    if fst_results and fst_results[0]['tags'][0] != 'UNK':
        if len(fst_results) == 1 or gnn_disamb is None:
            # Only one candidate or no GNN available
            return [
                {
                    "root": res['lemma'],
                    "gloss": "",
                    "analysis": res['analysis'],
                    "tags": res['tags']
                } for res in fst_results
            ]
        # Use GNN to select best candidate
        best = gnn_disamb.disambiguate(fst_results)
        return [{
            "root": best['lemma'],
            "gloss": "",
            "analysis": best['analysis'],
            "tags": best['tags']
        }]
    # Fallback to lexical dictionary lookup
    lex = analyze_word_lexical(word)
    tags = [lex.get('POS', 'UNK')] + [f"{k}={v}" for k, v in lex.get('features', {}).items()]
    return [{
        "root": word,
        "gloss": "",
        "analysis": word,
        "tags": tags
    }]
