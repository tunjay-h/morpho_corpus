# core/models.py
"""
Machine learning-based morphological tagger.
"""
import os
import pickle
from typing import List, Tuple

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from db.corpus import get_corpus

MODEL_PATH = "models/tag_predictor.pkl"

def prepare_dataset() -> Tuple[List[str], List[str]]:
    """
    Prepare training data from the annotated corpus.
    Returns X (words) and y (tag sequences).
    """
    corpus = get_corpus()
    X, y = [], []
    for entry in corpus:
        for token in entry["tokens"]:
            word = token.get("word")
            tags = token.get("tags", [])
            if tags:
                X.append(word)
                y.append("+".join(tags))
    return X, y

def train_tag_predictor() -> Pipeline:
    """
    Train and save a morphological tagger on the corpus.
    """
    X, y = prepare_dataset()
    if not X:
        print("Corpus is empty. Cannot train model.")
        return None

    pipeline = Pipeline([
        ("vect", CountVectorizer(analyzer="char", ngram_range=(2, 4))),
        ("clf", LogisticRegression(max_iter=500))
    ])
    pipeline.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    print(f"Model saved to: {MODEL_PATH}")
    return pipeline

def predict_tags(word: str) -> List[str]:
    """
    Predict morphological tags for a single word using the trained model.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained. Call train_tag_predictor() first.")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    predicted = model.predict([word])[0]
    return predicted.split("+")
