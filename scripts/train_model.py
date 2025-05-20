# scripts/train_model.py — script to train the morphological tagger
from core.models import train_tag_predictor

import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    model = train_tag_predictor()
    if model:
        logging.info("Model training complete.")
        print("Model training complete.")
    else:
        logging.warning("Model training failed. Is the corpus populated?")
        print("Model training failed. Is the corpus populated?")
