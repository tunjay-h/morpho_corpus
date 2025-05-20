# Data Directory

This directory contains the core data resources for Azerbaijani morphological analysis.

## Files
- `roots.json` — Root lexicon (word stems and their features)
- `affixes.json` — Affix lexicon (suffixes, prefixes, infixes)
- `rules.json` — Morphological rules for analysis and generation
- `tag_vocab.json` — Tag vocabulary for GNN and ML models
- `gnn_train.jsonl` — Training data for GNN disambiguator

## Validation
- All JSON files should be valid UTF-8 encoded and follow standard JSON schema.
- Each lexicon/rule file should be a dictionary or list as appropriate; see code docstrings for expected structure.

## Example
```json
{
  "yaz": {"pos": "VERB", "features": ["PAST"]},
  "ev": {"pos": "NOUN", "features": ["LOC"]}
}
```

## Notes
- If you add new resources, update this README accordingly.
