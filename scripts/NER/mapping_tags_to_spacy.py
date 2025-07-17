import os
import re

# Mapping AMI tags to spaCy-style NER tags
AMI_TO_SPACY = {
    # ENAMEX
    "PROJECT_MANAGER": "PERSON",
    "INTERFACE_SPECIALIST": "PERSON",
    "MARKETING": "PERSON",
    "INDUSTRIAL_DESIGNER": "PERSON",
    "PARTICIPANT": "PERSON",
    "EXPERIMENTER": "PERSON",
    "OTHER": "PERSON",
    "PERSON": "PERSON",
    "LOCATION": "LOC",
    "ORGANIZATION": "ORG",
    # TIMEX
    "TIME": "TIME",
    "DATE": "DATE",
    "DURATION": "TIME",
    # NUMEX
    "MONEY": "MONEY",
    "MEASURE": "QUANTITY",
    "PERCENT": "PERCENT",
    "CARDINAL": "CARDINAL",
    # ARTEFACT
    "FURNITURE": "PRODUCT",
    "MEANS_OF_WORKING": "PRODUCT",
    "RECORDING_DEVICES": "PRODUCT",
    "MODELLING_STUFF": "PRODUCT",
    "INCIDENTAL": "PRODUCT",
    "CONSTRUCTED": "PRODUCT",
    "DRAWING": "PRODUCT",
    # Others
    "COLOUR": "MISC",
    "SHAPE": "MISC",
    "MATERIALS": "MISC"
}

def map_ner_label(ami_label):
    """Map a fine-grained AMI label to a coarser spaCy-compatible tag."""
    return AMI_TO_SPACY.get(ami_label, "MISC")

def convert_ner_mapping_file(input_path, output_path):
    """Convert one NER mapping file from AMI tags to spaCy tags."""
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line or "->" not in line:
                continue
            try:
                phrase, label_part = line.split("->")
                phrase = phrase.strip()
                ami_label = re.sub(r"[\[\]\s]", "", label_part)
                spacy_label = map_ner_label(ami_label)
                fout.write(f"{phrase} -> [{spacy_label}]\n")
            except Exception as e:
                print(f"⚠️ Skipping line: {line} — Error: {e}")

def convert_directory(input_dir, output_dir):
    """Convert all files in the input directory and write mapped output files."""
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.endswith(".txt"):
            input_path = os.path.join(input_dir, fname)
            output_path = os.path.join(output_dir, fname)
            print(f"🔁 Converting: {fname}")
            convert_ner_mapping_file(input_path, output_path)

    print(f"\n✅ All files processed and saved to: {output_dir}")

# ✨ Entry point
if __name__ == "__main__":
    input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER"
    output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\spacyMapped"

    convert_directory(input_dir, output_dir)


    
