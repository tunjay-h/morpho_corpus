# ui/annotator.py
"""
Annotator UI for Azerbaijani morphological annotation.
"""
import gradio as gr
from core.tokenizer import prepare_input
from core.engine import analyze_word
from db.corpus import add_entry


import logging

def analyze_text(sentence: str):
    """
    Tokenize and analyze sentence, return table of word/tag pairs.
    Logs the process and errors.
    """
    try:
        tokens = prepare_input(sentence)
        table = []
        for tok in tokens:
            analyses = analyze_word(tok)
            if analyses and "error" not in analyses[0]:
                tags = analyses[0].get("tags", [])
            else:
                tags = []
            table.append([tok, "+".join(tags)])
        logging.info(f"Analyzed sentence: '{sentence[:40]}...' -> {table}")
        return table
    except Exception as e:
        logging.error(f"Failed to analyze sentence '{sentence}': {e}")
        return []


def save_to_corpus(sentence: str, data):
    """
    Save edited annotations to corpus. Logs the operation and errors.
    """
    try:
        tokens = []
        for row in data:
            word, tag_str = row
            tags = tag_str.split("+") if tag_str else []
            tokens.append({"word": word, "tags": tags})
        add_entry(sentence, tokens)
        logging.info(f"Saved annotation for: '{sentence[:40]}...' with {len(tokens)} tokens.")
        return "Annotation saved to corpus."
    except Exception as e:
        logging.error(f"Failed to save annotation for '{sentence}': {e}")
        return "Failed to save annotation."


with gr.Blocks() as app:
    gr.Markdown("## Azerbaijani Morphological Annotator")
    sentence_input = gr.Textbox(label="Enter sentence", placeholder="Type Azerbaijani text here...")
    analyze_btn = gr.Button("Analyze")
    token_table = gr.Dataframe(
        headers=["Word", "Tags"],
        row_count=(1, "dynamic"),
        col_count=2,
        interactive=True
    )
    save_btn = gr.Button("Save to Corpus")
    status = gr.Textbox(label="Status", interactive=False)

    analyze_btn.click(analyze_text, inputs=sentence_input, outputs=token_table)
    save_btn.click(save_to_corpus, inputs=[sentence_input, token_table], outputs=status)

if __name__ == "__main__":
    app.launch()
