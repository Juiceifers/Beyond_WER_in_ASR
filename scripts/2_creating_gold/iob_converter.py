import os
import json
from nltk.tokenize import word_tokenize
from tqdm import tqdm


def load_gold_entities(entity_file):
    """Loads gold NER entity lines from a .ner.gold.txt file"""
    entities = []
    with open(entity_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '->' not in line:
                continue
            text, label = line.strip().split('->')
            ent_text = text.strip()
            ent_label = label.strip()[1:-1]  # remove square brackets
            entities.append((ent_text, ent_label))
    return entities


def convert_gold_txt_to_iob(ner_gold_txt_path):
    """Converts each gold NE entry to IOB-tagged tokens"""
    entities = load_gold_entities(ner_gold_txt_path)
    iob_tokens = []

    for ent_text, ent_label in entities:
        tokens = word_tokenize(ent_text)
        for i, token in enumerate(tokens):
            prefix = 'B-' if i == 0 else 'I-'
            iob_tokens.append((token, prefix + ent_label))

    return iob_tokens


def batch_convert_gold_txt_dir_to_iob(input_ner_txt_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ner_files = [f for f in os.listdir(input_ner_txt_dir) if f.endswith(".ner.gold.txt")]

    for fname in tqdm(ner_files, desc="Converting .ner.gold.txt to IOB"):
        base = fname.replace(".ner.gold.txt", "")
        ner_path = os.path.join(input_ner_txt_dir, fname)
        output_iob_path = os.path.join(output_dir, f"{base}.iob.txt")

        iob_tags = convert_gold_txt_to_iob(ner_path)

        with open(output_iob_path, 'w', encoding='utf-8') as out:
            for token, label in iob_tags:
                out.write(f"{token}\t{label}\n")

    print(f"\n✅ Done! IOB files saved in: {output_dir}")


if __name__ == "__main__":
    INPUT_NER_TXT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER"
    OUTPUT_IOB_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\IOB_format"

    batch_convert_gold_txt_dir_to_iob(INPUT_NER_TXT_DIR, OUTPUT_IOB_DIR)
