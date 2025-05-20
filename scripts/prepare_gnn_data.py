"""
scripts/prepare_gnn_data.py

Utility to convert a corpus with gold analyses into GNN training format (JSONL).
Each line: {"analyses": [...], "gold_idx": int}
"""
import json, os
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_corpus(path: str) -> Dict:
    """
    Load a corpus from a JSON file.

    Args:
        path (str): Path to the corpus JSON file.

    Returns:
        Dict: The loaded corpus.
    """
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load corpus from {path}: {e}")
        raise

def load_fst_candidates(word: str) -> List[Dict]:
    """
    Load FST candidates for a given word.

    Args:
        word (str): The word to analyze.

    Returns:
        List[Dict]: The FST candidates.
    """
    try:
        from core.fst_engine import FSTEngine
        fst = FSTEngine(fst_bin_path=None)
        return fst.analyze(word)
    except Exception as e:
        logging.error(f"Failed to load FST candidates for {word}: {e}")
        raise

def main(corpus_path: str, out_path: str) -> None:
    """
    Prepare GNN data from a corpus.

    Args:
        corpus_path (str): Path to the corpus JSON file.
        out_path (str): Path to the output JSONL file.
    """
    try:
        corpus = load_corpus(corpus_path)
        count = 0
        with open(out_path, 'w', encoding='utf-8') as f:
            for entry in corpus:
                word = entry['word']
                gold_analysis = entry['analysis']
                candidates = load_fst_candidates(word)
                if not candidates:
                    continue
                gold_idx = next((i for i, c in enumerate(candidates) if c['analysis'] == gold_analysis), -1)
                if gold_idx == -1:
                    continue  # skip if gold not in candidates
                item = {'analyses': candidates, 'gold_idx': gold_idx}
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                count += 1
        logging.info(f"Prepared GNN data: {count} examples written to {out_path}")
    except Exception as e:
        logging.error(f"Failed to prepare GNN data: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', required=True, help='Path to corpus JSON')
    parser.add_argument('--out', required=True, help='Output JSONL for GNN training')
    args = parser.parse_args()
    main(args.corpus, args.out)
