import os
import re

# -------------------------------
# Contraction Expansion Dictionary
# -------------------------------
CONTRACTION_MAP = {
    "it's": "it is", "don't": "do not", "i'm": "i am", "you're": "you are",
    "he's": "he is", "she's": "she is", "they're": "they are", "we're": "we are",
    "isn't": "is not", "aren't": "are not", "wasn't": "was not", "weren't": "were not",
    "can't": "cannot", "couldn't": "could not", "won't": "will not", "wouldn't": "would not",
    "shouldn't": "should not", "didn't": "did not", "hasn't": "has not", "haven't": "have not",
    "hadn't": "had not", "there's": "there is", "there're": "there are", "let's": "let us",
    "that's": "that is", "what's": "what is", "who's": "who is", "how's": "how is",
    "could've": "could have", "would've": "would have", "should've": "should have",
    "might've": "might have", "must've": "must have",
    "you'll": "you will", "i'll": "i will", "he'll": "he will", "she'll": "she will",
    "we'll": "we will", "they'll": "they will", "i'd": "i would", "you'd": "you would",
    "he'd": "he would", "she'd": "she would", "they'd": "they would", "we'd": "we would",
    "doesn't": "does not",
    "n't": " not", "'re": " are", "'ve": " have", "'d": " would", "'ll": " will",
    "'s": " is", "'m": " am", "gonna": "going to"
}

# -------------------------------
# Text Normalization Functions
# -------------------------------
def expand_contractions(text, contractions=CONTRACTION_MAP):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in contractions.keys()) + r')\b')
    return pattern.sub(lambda x: contractions[x.group(0)], text)

def normalize_text(text):
    text = text.lower().strip()
    text = expand_contractions(text)
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    return text

def normalize_files_in_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r', encoding='utf-8') as f:
                raw = f.read()

            normalized = normalize_text(raw)

            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(normalized)

            print(f"✅ Normalized: {filename}")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    # === SCENARIO BASED ===
    gold_scenario_dir = r"C:\path\to\gold_scripts\transcripts\scenario\original"
    hyp_scenario_dir  = r"C:\path\to\whisper_outputs\scenario\original"

    gold_scenario_out = r"C:\path\to\normalized_output\gold\scenario"
    hyp_scenario_out  = r"C:\path\to\normalized_output\hyp\scenario"

    # === NATURAL ===
    gold_natural_dir = r"C:\path\to\gold_scripts\transcripts\natural\original"
    hyp_natural_dir  = r"C:\path\to\whisper_outputs\natural\original"

    gold_natural_out = r"C:\path\to\normalized_output\gold\natural"
    hyp_natural_out  = r"C:\path\to\normalized_output\hyp\natural"

    # Process all
    normalize_files_in_directory(gold_scenario_dir, gold_scenario_out)
    normalize_files_in_directory(hyp_scenario_dir, hyp_scenario_out)

    normalize_files_in_directory(gold_natural_dir, gold_natural_out)
    normalize_files_in_directory(hyp_natural_dir, hyp_natural_out)
