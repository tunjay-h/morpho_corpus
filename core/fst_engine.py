"""
core/fst_engine.py

Scaffold for integrating FST-based morphological analysis for Azerbaijani.
This module will interface with external FST tools (HFST/Foma) and provide a Python API.
"""
import subprocess
import logging
from typing import List, Dict, Optional

class FSTEngine:
    """
    Wrapper for FST-based morphological analyzer.
    Uses HFST subprocess if available, otherwise falls back to simulated logic.
    """
    def __init__(self, fst_bin_path: Optional[str]):
        self.fst_bin_path = fst_bin_path  # Path to compiled FST analyzer
        if self.fst_bin_path:
            logging.info(f"FSTEngine initialized with binary: {self.fst_bin_path}")
        else:
            logging.warning("FSTEngine initialized in simulated mode (no FST binary)")

    def analyze(self, word: str) -> List[Dict]:
        """
        Analyze a word using HFST via subprocess if fst_bin_path is set; otherwise, use simulated logic.
        Returns a list of analyses (lemma, tags, segmentation).
        """
        if self.fst_bin_path:
            try:
                proc = subprocess.Popen(
                    ['hfst-lookup', self.fst_bin_path],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    encoding='utf-8'
                )
                out, err = proc.communicate(word + '\n')
                if err:
                    logging.error(f"HFST error for '{word}': {err}")
                analyses = []
                for line in out.splitlines():
                    if '\t' in line:
                        try:
                            surface, analysis = line.split('\t', 1)
                        except ValueError:
                            logging.warning(f"Malformed FST output line (expected one tab): {line}")
                            continue
                        if analysis.strip() == '':
                            continue
                        parts = analysis.strip().replace('\t', '+').split('+')
                        lemma = parts[0] if parts else word
                        tags = parts[1:] if len(parts) > 1 else []
                        analyses.append({'lemma': lemma, 'tags': tags, 'analysis': analysis.strip().replace('\t', '+')})
                if not analyses:
                    logging.info(f"No FST analysis for '{word}', returning UNK.")
                    return [{"lemma": word, "tags": ["UNK"], "analysis": word}]
                logging.info(f"FST analysis for '{word}': {analyses}")
                return analyses
            except Exception as e:
                logging.error(f"Exception in FSTEngine.analyze for '{word}': {e}")
                return [{"lemma": word, "tags": ["UNK"], "analysis": word}]
        # fallback: simulated logic
        try:
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
                logging.info(f"No simulated FST analysis for '{word}', returning UNK.")
                return [{"lemma": word, "tags": ["UNK"], "analysis": word}]
            logging.info(f"Simulated FST analysis for '{word}': {results}")
            return results
        except Exception as e:
            logging.error(f"Exception in simulated FSTEngine.analyze for '{word}': {e}")
            return [{"lemma": word, "tags": ["UNK"], "analysis": word}]


    def batch_analyze(self, words: List[str]) -> List[List[Dict]]:
        """
        Analyze a batch of words.
        Returns a list of analyses for each word.
        """
        return [self.analyze(w) for w in words]

# Example usage (to be replaced with real paths and logic):
# fst_engine = FSTEngine(fst_bin_path='analyzer.hfst')
# print(fst_engine.analyze('gəldim'))
