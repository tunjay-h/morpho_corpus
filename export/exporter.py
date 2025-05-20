# export/exporter.py
"""
Corpus exporters: CoNLL-U, Excel, JSONL, CSV.
"""
import os
import json
import csv
import pandas as pd
from db.corpus import get_corpus

# Paths
CONLLU_PATH = "corpus/corpus.conllu"
EXCEL_PATH = "corpus/corpus.xlsx"
JSONL_PATH = "corpus/corpus.jsonl"
CSV_PATH = "corpus/corpus.csv"


def export_to_conllu(path: str = CONLLU_PATH) -> str:
    """
    Export corpus to CoNLL-U format. Logs success and errors.
    """
    corpus = get_corpus()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for i, entry in enumerate(corpus, start=1):
                f.write(f"# sent_id = {i}\n")
                f.write(f"# text = {entry['text']}\n")
                for idx, tok in enumerate(entry["tokens"], start=1):
                    word = tok["word"]
                    lemma = tok.get("lemma", word.lower())
                    tags = tok.get("tags", [])
                    upos = tags[0] if tags else "X"
                    feats = "|".join(tags[1:]) if len(tags) > 1 else "_"
                    f.write(f"{idx}\t{word}\t{lemma}\t{upos}\t_\t{feats}\t_\t_\t_\t_\n")
                f.write("\n")
        logging.info(f"Exported corpus to CoNLL-U format at {path}")
        return path
    except Exception as e:
        logging.error(f"Failed to export to CoNLL-U: {e}")
        return ""


def export_to_excel(path: str = EXCEL_PATH) -> str:
    """
    Export corpus to Excel format. Logs success and errors.
    """
    corpus = get_corpus()
    try:
        data = []
        for entry in corpus:
            for tok in entry["tokens"]:
                data.append({"text": entry["text"], **tok})
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_excel(path, index=False)
        logging.info(f"Exported corpus to Excel at {path}")
        return path
    except Exception as e:
        logging.error(f"Failed to export to Excel: {e}")
        return ""


def export_to_jsonl(path: str = JSONL_PATH) -> str:
    """
    Export corpus to JSONL format. Logs success and errors.
    """
    corpus = get_corpus()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for entry in corpus:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def export_to_csv(path: str = CSV_PATH) -> str:
    """Export corpus to simple CSV format."""
    corpus = get_corpus()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sentence", "token", "lemma", "upos", "features"])
        for entry in corpus:
            for token in entry["tokens"]:
                word = token["word"]
                lemma = token.get("lemma", word.lower())
                tags = token.get("tags", [])
                upos = tags[0] if tags else "X"
                feats = "|".join(tags[1:]) if len(tags) > 1 else "_"
                writer.writerow([entry["text"], word, lemma, upos, feats])
    return path
