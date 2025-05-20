"""
tests/test_hybrid_pipeline.py

Test script for the end-to-end hybrid FST+GNN morphological analysis pipeline.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import analyze_word

def test_examples():
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
        assert any(gold in r["analysis"] for r in result), f"Failed on {word}: got {result}"
        print(f"{word}: PASS ({result})")

if __name__ == "__main__":
    test_examples()
    print("All tests passed!")
