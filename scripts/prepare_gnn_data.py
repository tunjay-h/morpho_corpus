"""
scripts/prepare_gnn_data.py

Utility to convert a corpus with gold analyses into GNN training format (JSONL).
Each line: {"analyses": [...], "gold_idx": int}
"""
import json, os
from typing import List, Dict

def load_corpus(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_fst_candidates(word: str):
    from core.fst_engine import FSTEngine
    fst = FSTEngine(fst_bin_path=None)
    return fst.analyze(word)

def main(corpus_path, out_path):
    corpus = load_corpus(corpus_path)
    with open(out_path, 'w', encoding='utf-8') as fout:
        for entry in corpus:
            word = entry['word']
            gold_analysis = entry['analysis']
            candidates = load_fst_candidates(word)
            if not candidates:
                continue
            gold_idx = next((i for i, c in enumerate(candidates) if c['analysis'] == gold_analysis), -1)
            if gold_idx == -1:
                continue  # skip if gold not in candidates
            fout.write(json.dumps({"analyses": candidates, "gold_idx": gold_idx}) + '\n')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', required=True, help='Path to corpus JSON')
    parser.add_argument('--out', required=True, help='Output JSONL for GNN training')
    args = parser.parse_args()
    main(args.corpus, args.out)
