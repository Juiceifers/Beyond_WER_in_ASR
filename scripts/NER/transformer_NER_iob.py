import os
from tqdm import tqdm
from transformers import pipeline


ner_pipeline_bert = pipeline("ner", model="dslim/bert-base-NER", tokenizer="bert-base-cased", grouped_entities=True)
ner_pipeline_roberta = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", tokenizer="Jean-Baptiste/roberta-large-ner-english", grouped_entities=True )


def run_ner_on_text(text, model):
    results = model(text)
    entities = []

    for ent in results:
        label = ent["entity_group"]
        word = ent["word"]
        entities.append({
            "text": word,
            "label": label
        })
    #print(f"\n{entities}\n")
    return entities



def batch_run_ner(input_dir, output_dir):
    """Run NER over all .txt files and save outputs per model"""
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for fname in tqdm(files, desc="Running Transformer NER"):
        input_path = os.path.join(input_dir, fname)
        base = fname.replace(".txt", "")

        bert_out_path = os.path.join(output_dir, "bert", f"{base}.ner.jsonl")
        roberta_out_path = os.path.join(output_dir, "roberta", f"{base}.ner.jsonl")
        os.makedirs(os.path.dirname(bert_out_path), exist_ok=True)
        os.makedirs(os.path.dirname(roberta_out_path), exist_ok=True)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        ner_entities_bert = run_ner_on_text(text, ner_pipeline_bert)
        ner_entities_roberta = run_ner_on_text(text, ner_pipeline_roberta)


        with open(bert_out_path, "w", encoding="utf-8") as out:
            for ent in ner_entities_bert:
                out.write(f"{ent['text']}\t{ent['label']}\n")
        with open(roberta_out_path, "w", encoding="utf-8") as out:
            for ent in ner_entities_roberta:
                out.write(f"{ent['text']}\t{ent['label']}\n")


    print(f"\nNER outputs from BERT and ROBERTA saved to:⬇️\n{output_dir}\n")



if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized_p"
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\transformer"

    batch_run_ner(INPUT_DIR, OUTPUT_DIR)

