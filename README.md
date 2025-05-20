# Azerbaijani Morphological Analysis Toolkit

This toolkit provides a complete pipeline for rule-based and ML-based morphological analysis and annotation of Azerbaijani text. It includes modular components for loading lexicons, tokenization, analysis, annotation GUIs, corpus storage, and export utilities.

## Features

- **Dictionary Loader (`loaders/dictionary_loader.py`)**
  - Load JSON lexicons for roots, affixes, and rules.
- **Text Preprocessing (`core/tokenizer.py`)**
  - Unicode-aware tokenization, normalization, and diacritics removal.
- **Rule-Based Engine (`core/engine.py`)**
  - Perform morphological analysis using lexicon and valid affix order.
- **ML Tagger (`core/models.py`)**
  - Train and predict morphological tags using scikit-learn.
- **Annotation UIs (`ui/annotator.py`, `ui/trainer.py`)**
  - Web interfaces powered by Gradio for manual annotation and model training.
- **Corpus Storage (`db/corpus.py`)**
  - Save, load, and append annotated sentences in `corpus/corpus.json`.
- **Export Utilities (`export/exporter.py`)**
  - Export annotated corpus to CoNLL-U, Excel, JSONL, and CSV formats.
- **Scripts (`scripts/train_model.py`)**
  - Command-line script to train the tag predictor.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/morpho_corpus.git
   cd morpho_corpus
   ```
2. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Directory Structure

```
morpho_corpus/                # project root
├─ data/                      # static lexicons (roots.json, affixes.json, rules.json)
├─ dictionaries/              # language-specific user dictionaries (az.json, tr.json, ru.json)
├─ loaders/                   # JSON lexicon loader module
│   └─ dictionary_loader.py
├─ core/                      # core processing
│   ├─ tokenizer.py           # Unicode tokenizer and normalization
│   ├─ engine.py              # rule-based analysis engine
│   └─ models.py              # ML tagger: train & predict
├─ ui/                        # Gradio-based GUIs
│   ├─ annotator.py           # browser UI for annotation
│   └─ trainer.py             # train tagger via web
├─ db/                        # corpus persistence
│   └─ corpus.py              # load, save, append annotations
├─ export/                    # export tools
│   └─ exporter.py            # export to CoNLL-U, Excel, JSONL, CSV
├─ scripts/                   # CLI scripts
│   └─ train_model.py         # train model script
├─ corpus/                    # user-generated data
│   ├─ corpus.json            # annotated data
│   └─ corpus.conllu          # exported CoNLL-U
├─ README.md                  # this file
├─ requirements.txt           # Python dependencies
└─ pyproject.toml             # project metadata
```

## Quick Start

1. **Annotate text:**
   ```bash
   python -m ui.annotator
   ```
   Enter an Azerbaijani sentence, click **Analyze**, edit tags, then **Save to Corpus**.

2. **Train ML tagger:**
   ```bash
   python -m ui.trainer
   ```
   Click **Train** to fit a character-ngram logistic regression model on your corpus.

3. **Export corpus:**
   ```python
   from export.exporter import (
       export_to_conllu, export_to_excel,
       export_to_jsonl, export_to_csv
   )

   print(export_to_conllu())  # saves and returns path
   ```

## Future Work

- **FST-based Morphological Engine**
  - Research and compare FST frameworks: [Pynini](https://github.com/kylebgorman/pynini), Foma, OpenFst.
  - Define morphology grammar (LEXC/XFST or Pynini) for roots and affixes.
  - Compile grammar into binary FST and integrate via a new `core/fst_engine.py` module.
  - Expose `analyze_word_fst()` API alongside rule-based and lexical engines.
  - Benchmark and validate FST output against existing analyses.
- **Testing & Validation**
  - Expand unit tests to cover FST engine and edge cases.
  - Automate regression tests for known word analyses.

---

## Hybrid FST + GNN Morphological Engine Roadmap

This project aims to combine the precision of Finite State Transducers (FST) with the learning power of Graph Neural Networks (GNN) for robust Azerbaijani morphological analysis.

### Summary
- **FST**: Handles regular, rule-based morphology and phonological alternations.
- **GNN**: Learns to disambiguate FST outputs, handle irregularities, and improve accuracy using annotated data.
- **Hybrid Pipeline**: FST generates all possible analyses; GNN selects the most probable analysis using context and learned patterns.

### Recommended Libraries & Tools
- **FST:** [HFST (Helsinki Finite-State Technology)](https://hfst.github.io/) or [Foma](https://fomafst.github.io/) (**recommended** for FST compilation and analysis)
- **GNN & Deep Learning:** [PyTorch](https://pytorch.org/) (**recommended**) with [torch_geometric](https://pytorch-geometric.readthedocs.io/) (preferred) or [DGL](https://www.dgl.ai/)
- **API:** [FastAPI](https://fastapi.tiangolo.com/) (**recommended** for RESTful API integration)
- **Containerization:** [Docker](https://www.docker.com/) (**recommended** for deployment)

### Developer Action List

#### Phase 1: Project Setup & Data Acquisition
- [ ] Choose and install FST toolkit (**HFST** or **Foma** recommended).
- [ ] Install **PyTorch** and a GNN library (**torch_geometric** or DGL).
- [ ] Gather/expand Azerbaijani root and affix lexicons, including irregular forms.
- [ ] Document morphological paradigms and phonological rules (vowel harmony, assimilation, etc.).
- [ ] Collect and annotate a morphological corpus (segmentation, lemma, features, gold analyses).

#### Phase 2: FST Component
- [ ] Design two-level FST (lexicon, morphotactics, phonological rules).
- [ ] Encode roots, affixes, and irregulars using flag diacritics for alternations.
- [ ] Implement morphotactic rules for valid morpheme sequences.
- [ ] Encode phonological rules for Azerbaijani-specific alternations.
- [ ] Compile and test FST on sample words; output all analyses for ambiguous forms.

#### Phase 3: GNN Component
- [ ] Define GNN architecture for disambiguation (**GCN/GAT** layers, possibly with **LSTM/Transformer** for context).
- [ ] Prepare training data: For each word, pair FST outputs with gold-standard analysis.
- [ ] Build graph representations (nodes: morphemes/features, edges: sequence/dependency).
- [ ] Train GNN to select the correct analysis; evaluate with accuracy, F1, etc.

#### Phase 4: Integration & API
- [ ] Create `core/fst_engine.py` to interface with FST toolkit and output analyses.
- [ ] Integrate FST and GNN: FST → GNN → final analysis.
- [ ] Wrap the hybrid engine in a Python module and/or REST API (**FastAPI** recommended).
- [ ] Add regression and unit tests for the hybrid pipeline.

#### Phase 5: Deployment & Maintenance
- [ ] Containerize the application (**Docker**).
- [ ] Document FST rules, GNN architecture, and API usage.
- [ ] Set up CI/CD for automated testing and deployment.
- [ ] Plan for periodic updates to lexicons, rules, and retraining models.

---

## Contributing

- Add new roots, affixes, or rules in `data/`.
- Expand language dictionaries in `dictionaries/`.
- Write unit tests under a `tests/` directory.
- Submit pull requests with clear descriptions.

## License

This project is licensed under the MIT License.