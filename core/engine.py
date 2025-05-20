# core/engine.py
"""
Rule-based morphological engine for Azerbaijani.
"""
from typing import List, Dict
from loaders.dictionary_loader import load_roots, load_affixes, load_rules
from core.lexical_tagger import analyze_word_lexical


def analyze_word(word: str) -> List[Dict]:
    """Perform rule-based morphological analysis of a single word."""
    roots = load_roots()
    affixes = load_affixes()
    rules = load_rules().get("valid_order", [])
    results: List[Dict] = []
    for root, data in roots.items():
        if word.startswith(root):
            remaining = word[len(root):]
            tags: List[str] = []
            form = root
            while remaining:
                matched = False
                for affix in sorted(affixes.keys(), key=lambda x: -len(x)):
                    if remaining.startswith(affix):
                        tag = affixes[affix].get("tag", affix)
                        tags.append(tag)
                        form += "+" + affix
                        remaining = remaining[len(affix):]
                        matched = True
                        break
                if not matched:
                    break
            if not remaining:
                results.append({
                    "root": root,
                    "gloss": data.get("gloss", ""),
                    "analysis": form,
                    "tags": tags
                })
    if not results:
        # Fallback to lexical dictionary lookup
        lex = analyze_word_lexical(word)
        tags = [lex.get('POS', 'UNK')] + [f"{k}={v}" for k, v in lex.get('features', {}).items()]
        return [{
            "root": word,
            "gloss": "",
            "analysis": word,
            "tags": tags
        }]
    return results
