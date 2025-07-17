import os
import re

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)     # collapse whitespace
    return text.strip()

def normalize_p(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)     # collapse whitespace
    return text.strip()

def normalize_file(input_path, output_path, output_path_p):
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    normalized_text = normalize(original_text)
    normalized_text_p = normalize_p(original_text)

    # Save punctuation-stripped version
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(normalized_text + "\n")

    # Save punctuation-preserving version
    os.makedirs(os.path.dirname(output_path_p), exist_ok=True)
    with open(output_path_p, "w", encoding="utf-8") as f:
        f.write(normalized_text_p + "\n")

    print(f"✅ Normalized (no punct) saved at: {output_path}")
    print(f"✅ Normalized (with punct) saved at: {output_path_p}")

def normalize_dir(input_dir, output_dir):
    '''
    Normalize all .txt files in input_dir and write two outputs:
    - one to output_dir with '_normalized.txt'
    - one to output_dir/normalized_p with '_normalized.txt'
    '''
    os.makedirs(output_dir, exist_ok=True)
    output_dir_p = os.path.join(output_dir, "normalized_p")
    os.makedirs(output_dir_p, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            base, ext = os.path.splitext(filename)
            output_filename = base + "_normalized" + ext

            output_path = os.path.join(output_dir, output_filename)
            output_path_p = os.path.join(output_dir_p, output_filename)

            normalize_file(input_path, output_path, output_path_p)

if __name__ == "__main__":
    print("🔁 Normalizing Gold Scripts")
    input_dir_gold = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural"
    output_dir_gold = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\normalized"
    os.makedirs(output_dir_gold, exist_ok=True)
    normalize_dir(input_dir_gold, output_dir_gold)

    print("\n🔁 Normalizing Whisper Outputs")
    input_dir_whisper = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural"
    output_dir_whisper = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\normalized"
    os.makedirs(output_dir_whisper, exist_ok=True)
    normalize_dir(input_dir_whisper, output_dir_whisper)
