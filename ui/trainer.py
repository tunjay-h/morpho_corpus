# ui/trainer.py
"""
Train UI for the morphological tagger.
"""

import gradio as gr
from core.models import train_tag_predictor

import logging

def train_model_interface() -> str:
    """
    Train tagger on the current corpus and report status. Logs events and errors.
    """
    try:
        model = train_tag_predictor()
        if model:
            logging.info("Training completed. Model saved.")
            return "Training completed. Model saved."
        logging.warning("Failed to train model. Corpus might be empty.")
        return "Failed to train model. Corpus might be empty."
    except Exception as e:
        logging.error(f"Training failed: {e}")
        return f"Training failed: {e}"

iface = gr.Interface(
    fn=train_model_interface,
    inputs=[],
    outputs="text",
    title="Train Morphological Tagger",
    description="Click to train the ML tagger on the current corpus."
)

if __name__ == "__main__":
    iface.launch()
