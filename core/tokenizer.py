# core/tokenizer.py
"""
Tokenizer and normalization for Azerbaijani text.
"""
import re
import unicodedata
from typing import List

# Pattern matching letters and digits including Azerbaijani-specific characters
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9ĞÜŞÖÇƏığüşıöçə]+", re.UNICODE)

def tokenize(text: str) -> List[str]:
    """
    Split input text into tokens of letters and digits.
    Normalizes to NFC form before tokenizing.
    """
    normalized_text = unicodedata.normalize("NFC", text)
    return TOKEN_PATTERN.findall(normalized_text)


def normalize(token: str) -> str:
    """
    Normalize a token by converting to lowercase and stripping diacritics.
    """
    token_lower = token.lower()
    # Decompose Unicode and remove combining marks
    decomposed = unicodedata.normalize("NFD", token_lower)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped)


def prepare_input(text: str) -> List[str]:
    """
    Full pipeline: tokenize and then normalize each token.
    Returns a list of clean tokens.
    """
    raw_tokens = tokenize(text)
    return [normalize(tok) for tok in raw_tokens]
