import os
from tqdm import tqdm
from transformers import pipeline


ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", tokenizer="bert-base-cased", grouped_entities=True)


def batch_run_ner(input_dir, output_dir):
    """Run NER over all .txt files and save outputs per model"""
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for fname in tqdm(files, desc="Running Transformer NER"):
        input_path = os.path.join(input_dir, fname)
        base = fname.replace(".txt", "")

        # Correct path construction
        test_out_path = os.path.join(output_dir, "test", f"{base}.ner.jsonl")

        # Ensure subdirectories exist
        os.makedirs(os.path.dirname(test_out_path), exist_ok=True)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"\n{ner_pipeline(text)}")
        print(f"{text}\n")


        # Save raw NER output
        with open(test_out_path, "w", encoding="utf-8") as out:
            out.write(f"{ner_pipeline(text)}\n")


    print(f"\n✅ NER outputs saved to: {output_dir}")



if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized_p"
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\transformer"

    batch_run_ner(INPUT_DIR, OUTPUT_DIR)

    
