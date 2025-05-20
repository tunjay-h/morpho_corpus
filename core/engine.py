# core/engine.py
"""
Rule-based morphological engine for Azerbaijani.
"""
from typing import List, Dict
from loaders.dictionary_loader import load_roots, load_affixes, load_rules
from core.lexical_tagger import analyze_word_lexical
from core.fst_engine import FSTEngine

fst_engine = FSTEngine(fst_bin_path=None)  # Not used in simulated mode


def analyze_word(word: str) -> List[Dict]:
    """Perform FST-based morphological analysis of a single word, fallback to lexical if needed."""
    fst_results = fst_engine.analyze(word)
    if fst_results and fst_results[0]['tags'][0] != 'UNK':
        # Convert FST output to legacy format for compatibility
        return [
            {
                "root": res['lemma'],
                "gloss": "",
                "analysis": res['analysis'],
                "tags": res['tags']
            } for res in fst_results
        ]
    # Fallback to lexical dictionary lookup
    lex = analyze_word_lexical(word)
    tags = [lex.get('POS', 'UNK')] + [f"{k}={v}" for k, v in lex.get('features', {}).items()]
    return [{
        "root": word,
        "gloss": "",
        "analysis": word,
        "tags": tags
    }]
