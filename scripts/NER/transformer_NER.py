import os
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from transformers import pipeline


# HuggingFace NER pipeline
# ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
# ner_pipeline = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", grouped_entities=True)
# more powerful transformer-based NER model
# ner_pipeline = pipeline(
#     "ner",
#     model="Jean-Baptiste/roberta-large-ner-english",
#     tokenizer="Jean-Baptiste/roberta-large-ner-english",
#     grouped_entities=True
# )

ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    tokenizer="dslim/bert-base-NER",
    aggregation_strategy="simple"
)



def run_ner_on_text(text):
    """Run NER and return list of {'text', 'label'} dictionaries"""
    results = ner_pipeline(text)
    entities = []

    for ent in results:
        clean_text = ent["word"].strip()
        label = ent["entity_group"]
        entities.append({
            "text": clean_text,
            "label": label
        })
    return entities


def batch_run_ner(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for fname in tqdm(files, desc="Running BERT-ASR NER"):
        input_path = os.path.join(input_dir, fname)
        output_name = fname.replace(".txt", ".ner.jsonl")
        output_path = os.path.join(output_dir, output_name)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        ner_entities = run_ner_on_text(text)

        with open(output_path, "w", encoding="utf-8") as out:
            for ent in ner_entities:
                out.write(f"{ent['text']}\t{ent['label']}\n")

    print(f"\n✅ BERT-ASR NER outputs saved to: {output_dir}")

if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario"
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\transformer\bert_asr"

    batch_run_ner(INPUT_DIR, OUTPUT_DIR)
