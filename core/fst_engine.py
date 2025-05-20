"""
core/fst_engine.py

Scaffold for integrating FST-based morphological analysis for Azerbaijani.
This module will interface with external FST tools (HFST/Foma) and provide a Python API.
"""
import subprocess
from typing import List, Dict, Optional

class FSTEngine:
    """
    Wrapper for FST-based morphological analyzer.
    Assumes FST binary is compiled externally (e.g., with HFST or Foma).
    """
    def __init__(self, fst_bin_path: str):
        self.fst_bin_path = fst_bin_path  # Path to compiled FST analyzer

    def analyze(self, word: str) -> List[Dict]:
        """
        Simulate FST-based morphological analysis using roots, affixes, and rules from data/.
        Returns a list of analyses (lemma, tags, segmentation).
        """
        import os, json
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        roots = json.load(open(os.path.join(base_dir, 'roots.json'), encoding='utf-8'))
        affixes = json.load(open(os.path.join(base_dir, 'affixes.json'), encoding='utf-8'))
        rules = json.load(open(os.path.join(base_dir, 'rules.json'), encoding='utf-8'))['valid_order']
        results = []
        for root, rdata in roots.items():
            if word.startswith(root):
                remaining = word[len(root):]
                seg = root
                tags = [rdata['pos']]
                affix_seq = []
                # Try to greedily match affixes in valid order
                i = 0
                while remaining and i < len(rules):
                    found = False
                    for affix, adata in affixes.items():
                        if remaining.startswith(affix) and adata['tag'] == rules[i]:
                            seg += '+' + affix
                            tags.append(adata['tag'])
                            affix_seq.append(affix)
                            remaining = remaining[len(affix):]
                            found = True
                            break
                    if not found:
                        i += 1
                if not remaining:
                    results.append({
                        'lemma': root,
                        'tags': tags,
                        'analysis': seg
                    })
        if not results:
            # fallback: no analysis found
            return [{"lemma": word, "tags": ["UNK"], "analysis": word}]
        return results


    def batch_analyze(self, words: List[str]) -> List[List[Dict]]:
        """
        Analyze a batch of words.
        Returns a list of analyses for each word.
        """
        return [self.analyze(w) for w in words]

# Example usage (to be replaced with real paths and logic):
# fst_engine = FSTEngine(fst_bin_path='analyzer.hfst')
# print(fst_engine.analyze('gəldim'))
