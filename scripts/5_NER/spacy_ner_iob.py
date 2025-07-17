import os
import spacy
from nltk.tokenize import word_tokenize
from tqdm import tqdm

# Load both spaCy models
nlp_sm = spacy.load("en_core_web_sm")
nlp_trf = spacy.load("en_core_web_trf")


def run_spacy_ner(text, nlp):
    """Run spaCy NER and return IOB-tagged (token, label) tuples"""
    doc = nlp(text)
    iob_output = []

    for ent in doc.ents:
        tokens = word_tokenize(ent.text)
        label = ent.label_
        for i, token in enumerate(tokens):
            prefix = "B-" if i == 0 else "I-"
            iob_output.append((token, f"{prefix}{label}"))

    return iob_output


def batch_run_spacy_ner(input_dir, output_base_dir):
    """Run both spaCy models and save results into separate subdirectories"""
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for model_name, nlp_model in [("spacy_sm", nlp_sm), ("spacy_trf", nlp_trf)]:
        model_output_dir = os.path.join(output_base_dir, model_name)
        os.makedirs(model_output_dir, exist_ok=True)

        for fname in tqdm(files, desc=f"Running {model_name} NER"):
            input_path = os.path.join(input_dir, fname)
            output_name = fname.replace(".txt", f"_{model_name[-2:]}_iob.txt")
            output_path = os.path.join(model_output_dir, output_name)

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            iob_tags = run_spacy_ner(text, nlp_model)

            with open(output_path, "w", encoding="utf-8") as out:
                for token, label in iob_tags:
                    out.write(f"{token}\t{label}\n")

    print(f"\n✅ IOB-tagged outputs saved to subfolders in: {output_base_dir}")


if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario"
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy"

    batch_run_spacy_ner(INPUT_DIR, OUTPUT_DIR)
