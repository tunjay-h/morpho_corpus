# scripts/train_model.py — script to train the morphological tagger
from core.models import train_tag_predictor

if __name__ == "__main__":
    model = train_tag_predictor()
    if model:
        print("Model training complete.")
    else:
        print("Model training failed. Is the corpus populated?")
