# annotator_ui.py — морфоанализатор с редактируемыми тегами

import gradio as gr
from ml_models import analyze_word

def analyze_sentence(sentence, lang_code):
    words = sentence.strip().split()
    return [analyze_word(w, lang_code) for w in words]

iface = gr.Interface(
    fn=analyze_sentence,
    inputs=[
        gr.Textbox(label="Sentence"),
        gr.Dropdown(["az", "tr", "ru"], value="az", label="Language")
    ],
    outputs="json",
    title="Multilingual Morphological Analyzer"
)

if __name__ == "__main__":
    iface.launch()

####
import gradio as gr
from text_input import prepare_input
from ml_models import predict_tags
from corpus_db import add_entry

def analyze_and_prepare(text):
    tokens = prepare_input(text)
    analyzed = []
    for tok in tokens:
        try:
            tags = predict_tags(tok)
        except Exception:
            tags = ["UNK"]
        analyzed.append({"word": tok, "tags": tags})
    return analyzed

def analyze_text(text):
    global last_tokens
    last_tokens = analyze_and_prepare(text)
    return [(tok["word"], ", ".join(tok["tags"])) for tok in last_tokens]

def add_to_corpus(text, edited_table):
    tokens = []
    for row in edited_table:
        word = row[0]
        tags = [t.strip() for t in row[1].split(",") if t.strip()]
        tokens.append({"word": word, "tags": tags})
    add_entry(text, tokens)
    return "Добавлено в корпус."

last_tokens = []

with gr.Blocks() as app:
    gr.Markdown("## Морфологический анализатор с редактируемыми тегами")
    input_text = gr.Textbox(label="Введите предложение", placeholder="Mətn daxil edin...")
    analyze_btn = gr.Button("Анализировать")
    
    token_table = gr.Dataframe(
        headers=["Слово", "Теги"],
        col_count=(2, "fixed"),
        label="Результат анализа",
        interactive=True,
        wrap=True,
        max_rows=30
    )
    
    add_btn = gr.Button("Добавить в корпус")
    status = gr.Textbox(label="Статус", interactive=False)

    analyze_btn.click(fn=analyze_text, inputs=input_text, outputs=token_table)
    add_btn.click(fn=add_to_corpus, inputs=[input_text, token_table], outputs=status)

if __name__ == "__main__":
    app.launch()

###################
# annotator_ui.py — морфоанализатор с возможностью добавления в корпус

import gradio as gr
from text_input import prepare_input
from ml_models import predict_tags
from corpus_db import add_entry

def analyze_and_prepare(text):
    tokens = prepare_input(text)
    analyzed = []
    for tok in tokens:
        try:
            tags = predict_tags(tok)
        except Exception:
            tags = ["UNK"]
        analyzed.append({"word": tok, "tags": tags})
    return analyzed

def format_output(analyzed_tokens):
    formatted = ""
    for tok in analyzed_tokens:
        formatted += f"{tok['word']}: {', '.join(tok['tags'])}\n"
    return formatted.strip()

def analyze_text(text):
    global last_tokens
    last_tokens = analyze_and_prepare(text)
    return format_output(last_tokens)

def add_to_corpus(text):
    if not last_tokens:
        return "Сначала выполните анализ."
    add_entry(text, last_tokens)
    return "Добавлено в корпус."

last_tokens = []

with gr.Blocks() as app:
    gr.Markdown("## Морфологический анализатор (Азербайджанский язык)")
    input_text = gr.Textbox(label="Введите предложение", placeholder="Mətn daxil edin...")
    analyze_btn = gr.Button("Анализировать")
    output_box = gr.Textbox(label="Результат анализа", lines=10)
    add_btn = gr.Button("Добавить в корпус")
    status = gr.Textbox(label="Статус", interactive=False)

    analyze_btn.click(fn=analyze_text, inputs=input_text, outputs=output_box)
    add_btn.click(fn=add_to_corpus, inputs=input_text, outputs=status)

if __name__ == "__main__":
    app.launch()

################

# annotator_ui.py — шаблон модуля
# annotator_ui.py — веб-интерфейс для морфоанализа

import gradio as gr
from morpho_engine import analyze_word

def analyze_input(word):
    results = analyze_word(word)
    if "error" in results[0]:
        return f"Ошибка: {results[0]['error']}"
    output = ""
    for r in results:
        output += f"Корень: {r['root']} ({r['gloss']})\n"
        output += f"Анализ: {r['analysis']}\n"
        output += f"Теги: {' + '.join(r['tags'])}\n\n"
    return output.strip()

iface = gr.Interface(
    fn=analyze_input,
    inputs=gr.Textbox(label="Введите слово"),
    outputs=gr.Textbox(label="Результат разбора"),
    title="Морфологический разбор (Азербайджанский)",
    description="Агглютинативный морфоанализатор с поддержкой аффиксов"
)

if __name__ == "__main__":
    iface.launch()


