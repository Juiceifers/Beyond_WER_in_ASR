import os
import re


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

DISFLUENCIES = {"uh", "um", "uhm", "mm", "mm-hmm", "huh"}

def remove_disfluencies(text):
    for pattern in DISFLUENCIES:
        text = re.sub(pattern, '', text)
    # Clean leftover whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def expand_contractions(text, contractions=CONTRACTION_MAP):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in contractions.keys()) + r')\b')
    return pattern.sub(lambda x: contractions[x.group(0)], text)

def normalize_text_no_punct(text):
    text = text.lower()
    text = expand_contractions(text)
    text = remove_disfluencies(text)
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)     # collapse whitespace
    return text.strip()

def normalize_text_with_punct(text):
    text = text.lower()
    text = expand_contractions(text)
    text = remove_disfluencies(text)
    text = re.sub(r"\s+", " ", text)     # collapse whitespace
    return text.strip()


def normalize_file(input_path, output_path, output_path_p):
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    normalized_text = normalize_text_no_punct(original_text)
    normalized_text_p = normalize_text_with_punct(original_text)

    # Save punctuation-stripped version
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(normalized_text + "\n")

    # Save punctuation-preserving version
    os.makedirs(os.path.dirname(output_path_p), exist_ok=True)
    with open(output_path_p, "w", encoding="utf-8") as f:
        f.write(normalized_text_p + "\n")


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
    #SCENARIO based
    input_dir_gold_scenario = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario"
    output_dir_gold_scenario = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\FULLY_NORMALIZED"
    os.makedirs(os.path.dirname(output_dir_gold_scenario), exist_ok=True)
    normalize_dir(input_dir_gold_scenario, output_dir_gold_scenario)

    #NATURAL based
    input_dir_gold_natural = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural"
    output_dir_gold_natural = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\FULLY_NORMALIZED"
    os.makedirs(os.path.dirname(output_dir_gold_natural), exist_ok=True)
    normalize_dir(input_dir_gold_natural, output_dir_gold_natural)



    print("🔁 Normalizing Whisper Outputs")
    #SCENARIO based
    input_dir_hyp_scenario = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario"
    output_dir_hyp_scenario = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\FULLY_NORMALIZED"
    os.makedirs(os.path.dirname(output_dir_hyp_scenario), exist_ok=True)
    normalize_dir(input_dir_hyp_scenario, output_dir_hyp_scenario)

    #SCENARIO based
    input_dir_hyp_natural = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural"
    output_dir_hyp_natural = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\FULLY_NORMALIZED"
    os.makedirs(os.path.dirname(output_dir_hyp_natural), exist_ok=True)
    normalize_dir(input_dir_hyp_natural, output_dir_hyp_natural)