import re
import os

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


    "COLOUR": "MISC", 
    "SHAPE": "MISC",
    "MATERIALS": "MISC",
}


def map_ami_to_spacy(iob_tag):
    """
    Convert AMI IOB tag to spaCy-style IOB tag.
    """
    if iob_tag == 'O':
        return 'O'
    
    match = re.match(r"([BI])-(.+)", iob_tag)
    if match:
        prefix, label = match.groups()
        mapped_label = AMI_TO_SPACY.get(label, "MISC")  # fallback to MISC
        return f"{prefix}-{mapped_label}"
    else:
        return iob_tag

def convert_iob_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                fout.write("\n")
                continue
            try:
                token, tag = line.split('\t')
                mapped_tag = map_ami_to_spacy(tag)
                fout.write(f"{token}\t{mapped_tag}\n")
            except ValueError:
                fout.write(line + "\n")  # Skip or copy malformed line

def convert_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".iob.txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"🔁 Converting: {filename}")
            convert_iob_file(input_path, output_path)

    print("✅ All files converted and saved to:", output_dir)


if __name__ == "__main__":

    input_directory = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\IOB_format"
    output_directory = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\IOB_format\spacyMapped"

    convert_directory(input_directory, output_directory)
