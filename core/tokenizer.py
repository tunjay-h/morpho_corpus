# core/tokenizer.py
"""
Tokenizer and normalization for Azerbaijani text.
"""
import re
import unicodedata
from typing import List

# Pattern matching letters and digits including Azerbaijani-specific characters
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9ĞÜŞÖÇƏığüşıöçə]+", re.UNICODE)

import logging

def tokenize(text: str) -> List[str]:
    """
    Split input text into tokens of letters and digits.
    Normalizes to NFC form before tokenizing.
    Logs the result.
    """
    normalized_text = unicodedata.normalize("NFC", text)
    tokens = TOKEN_PATTERN.findall(normalized_text)
    logging.info(f"Tokenized '{text}' to {tokens}")
    return tokens


def normalize(token: str) -> str:
    """
    Normalize a token by converting to lowercase and stripping diacritics.
    Logs the result.
    """
    token_lower = token.lower()
    decomposed = unicodedata.normalize("NFD", token_lower)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    normalized = unicodedata.normalize("NFC", stripped)
    logging.info(f"Normalized '{token}' to '{normalized}'")
    return normalized


def prepare_input(text: str) -> List[str]:
    """
    Full pipeline: tokenize and then normalize each token.
    Returns a list of clean tokens. Logs the process.
    """
    raw_tokens = tokenize(text)
    normalized_tokens = [normalize(tok) for tok in raw_tokens]
    logging.info(f"Prepared input: {normalized_tokens}")
    return normalized_tokens
