"""
tests/test_hybrid_pipeline.py

Test script for the end-to-end hybrid FST+GNN morphological analysis pipeline.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import analyze_word

import logging

def test_examples():
    """
    Test hybrid pipeline on example words. Logs test results and assertion failures.
    """
    examples = [
        ("yazdı", "yaz+PAST"),
        ("oxuyacaq", "oxu+FUT"),
        ("gördüm", "gör+PAST"),
        ("kitablar", "kitab+PLUR"),
        ("evdə", "ev+LOC"),
        ("adamın", "adam+GEN"),
        ("uşaqlar", "uşaq+PLUR"),
        ("böyükdür", "böyük+CAUS")
    ]
    for word, gold in examples:
        result = analyze_word(word)
        try:
            assert any(gold in r["analysis"] for r in result), f"Failed on {word}: got {result}"
            logging.info(f"{word}: PASS ({result})")
            print(f"{word}: PASS ({result})")
        except AssertionError as e:
            logging.error(str(e))
            print(f"{word}: FAIL ({result})")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_examples()
    print("All tests completed!")
