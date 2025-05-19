# Повторно создаём файл corpus_db.py после сброса окружения

corpus_db_code = """
# corpus_db.py — хранение и обновление корпуса аннотированных слов

import json
import os

CORPUS_PATH = "corpus/corpus.json"

def load_corpus():
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_corpus(corpus):
    os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

def add_entry(text, tokens):
    \"\"\"Добавляет предложение и токены с анализами в корпус\"\"\"
    corpus = load_corpus()
    entry = {
        "text": text,
        "tokens": tokens
    }
    corpus.append(entry)
    save_corpus(corpus)

def get_corpus():
    return load_corpus()
"""

# Сохраняем в файл
os.makedirs("/mnt/data/morpho_corpus_template", exist_ok=True)
with open("/mnt/data/morpho_corpus_template/corpus_db.py", "w", encoding="utf-8") as f:
    f.write(corpus_db_code.strip())

"/mnt/data/morpho_corpus_template/corpus_db.py"


################
# corpus_db.py — шаблон модуля

# Повторно создаём файл corpus_db.py после сброса окружения
# corpus_db.py — хранение и обновление корпуса аннотированных слов

import json
import os

CORPUS_PATH = "corpus/corpus.json"

def load_corpus():
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_corpus(corpus):
    os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

def add_entry(text, tokens):
    """Добавляет предложение и токены с анализами в корпус"""
    corpus = load_corpus()
    entry = {
        "text": text,
        "tokens": tokens
    }
    corpus.append(entry)
    save_corpus(corpus)

def get_corpus():
    return load_corpus()

corpus_db_code = """
# corpus_db.py — хранение и обновление корпуса аннотированных слов

import json
import os

CORPUS_PATH = "corpus/corpus.json"

def load_corpus():
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_corpus(corpus):
    os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

def add_entry(text, tokens):
    \"\"\"Добавляет предложение и токены с анализами в корпус\"\"\"
    corpus = load_corpus()
    entry = {
        "text": text,
        "tokens": tokens
    }
    corpus.append(entry)
    save_corpus(corpus)

def get_corpus():
    return load_corpus()
"""

# Сохраняем в файл
os.makedirs("/mnt/data/morpho_corpus_template", exist_ok=True)
with open("/mnt/data/morpho_corpus_template/corpus_db.py", "w", encoding="utf-8") as f:
    f.write(corpus_db_code.strip())

"/mnt/data/morpho_corpus_template/corpus_db.py"
