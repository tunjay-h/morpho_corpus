# ui/trainer.py
"""
Train UI for the morphological tagger.
"""

import gradio as gr
from core.models import train_tag_predictor

def train_model_interface() -> str:
    """
    Train tagger on the current corpus and report status.
    """
    model = train_tag_predictor()
    if model:
        return "Training completed. Model saved."
    return "Failed to train model. Corpus might be empty."

iface = gr.Interface(
    fn=train_model_interface,
    inputs=[],
    outputs="text",
    title="Train Morphological Tagger",
    description="Click to train the ML tagger on the current corpus."
)

if __name__ == "__main__":
    iface.launch()
