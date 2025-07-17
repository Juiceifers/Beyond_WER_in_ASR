import os
import spacy
from tqdm import tqdm

# Load spaCy models
nlp_sm = spacy.load("en_core_web_sm")
nlp_trf = spacy.load("en_core_web_trf")

def extract_entities(text, nlp):
    """Return a list of (span_text, label) for all entities in the text."""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def batch_extract_entities(input_dir, output_base_dir):
    """Process text files using spaCy NER models and write span -> [LABEL] outputs"""
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for model_name, nlp_model in [("spacy_sm", nlp_sm), ("spacy_trf", nlp_trf)]:
        model_output_dir = os.path.join(output_base_dir, model_name)
        os.makedirs(model_output_dir, exist_ok=True)

        for fname in tqdm(files, desc=f"Running {model_name} NER"):
            input_path = os.path.join(input_dir, fname)
            output_name = fname.replace(".txt", f"_{model_name[-2:]}.txt")
            output_path = os.path.join(model_output_dir, output_name)

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            entities = extract_entities(text, nlp_model)

            with open(output_path, "w", encoding="utf-8") as out:
                for span_text, label in entities:
                    out.write(f"{span_text} -> [{label}]\n")

    print(f"\n✅ Outputs saved to subfolders in: {output_base_dir}")

if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario"
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy"

    batch_extract_entities(INPUT_DIR, OUTPUT_DIR)
