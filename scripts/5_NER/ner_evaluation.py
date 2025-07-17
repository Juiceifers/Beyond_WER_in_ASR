# finalized evaluation
# partial span matching + precision + recall + f1


import os
import csv
import pandas as pd
import re

import re

def get_meeting_id(filename):
    """Extract meeting ID like 'ES2016a' from any filename"""
    match = re.match(r'(ES\d{4}[a-z]|EN\d{4}[a-z])', filename)
    return match.group(1) if match else None


def load_ner_file(file_path):
    """
    Loads a NER file formatted like:
    Barack Obama -> PERSON
    Returns a list of (span, label)
    """
    ner_tuples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '->' not in line:
                continue
            try:
                span, label = line.strip().split('->')
                span = span.strip()
                label = label.strip().replace("[", "").replace("]", "")
                ner_tuples.append((span, label))
            except:
                continue
    return ner_tuples

def token_overlap(span1, span2):
    tokens1 = set(span1.lower().split())
    tokens2 = set(span2.lower().split())
    return len(tokens1 & tokens2) > 0

def evaluate_with_partial_match(gold_file, pred_file, verbose=True):
    gold = load_ner_file(gold_file)
    pred = load_ner_file(pred_file)

    matched = set()
    partial_matched = set()
    unmatched_pred = set(pred)
    unmatched_gold = set(gold)

    for g_span, g_label in gold:
        for p_span, p_label in pred:
            if g_label == p_label and g_span == p_span:
                matched.add((g_span, g_label))
                unmatched_pred.discard((p_span, p_label))
                unmatched_gold.discard((g_span, g_label))
                break
        else:
            for p_span, p_label in pred:
                if g_label == p_label and token_overlap(g_span, p_span):
                    partial_matched.add((g_span, g_label, p_span))
                    unmatched_pred.discard((p_span, p_label))
                    unmatched_gold.discard((g_span, g_label))
                    break

    exact = len(matched)
    partial = len(partial_matched)
    total_pred = len(pred)
    total_gold = len(gold)

    precision = (exact + partial) / total_pred if total_pred else 0.0
    recall = (exact + partial) / total_gold if total_gold else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    if verbose:
        print(f"\n📁 {os.path.basename(gold_file)}")
        print(f"✔️ Exact matches:   {exact}")
        print(f"🔸 Partial matches: {partial}")
        print(f"❌ Missed (gold):   {len(unmatched_gold)}")
        print(f"⚠️ Spurious (pred): {len(unmatched_pred)}")
        print(f"📊 Precision:       {precision:.2f}")
        print(f"📊 Recall:          {recall:.2f}")
        print(f"📊 F1-score:        {f1:.2f}\n")

    return {
        "file": os.path.basename(gold_file),
        "exact": exact,
        "partial": partial,
        "missed": len(unmatched_gold),
        "spurious": len(unmatched_pred),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }


def evaluate_all_and_save(gold_dir, pred_dir, output_dir, output_file):
    os.makedirs(output_dir, exist_ok=True)

    # Create mapping from meeting ID to predicted file
    pred_files = {get_meeting_id(f): f for f in os.listdir(pred_dir) if get_meeting_id(f)}

    results_all = []
    for gold_fname in os.listdir(gold_dir):
        meeting_id = get_meeting_id(gold_fname)
        if not meeting_id or meeting_id not in pred_files:
            print(f"❌ No matching prediction for {gold_fname}")
            continue

        gold_path = os.path.join(gold_dir, gold_fname)
        pred_path = os.path.join(pred_dir, pred_files[meeting_id])

        result = evaluate_with_partial_match(gold_path, pred_path, verbose=False)
        results_all.append(result)
        print(f"✅ Evaluated: {meeting_id}")


    if not results_all:
        print("⚠️ No evaluation results found. Check filename mapping.")
        return

    df = pd.DataFrame(results_all)
    df = df.sort_values(by="f1", ascending=False)

    output_path = os.path.join(output_dir, output_file)
    df.to_csv(output_path, index=False)
    print(f"✅ Results saved to: {output_path}")
    print(f"📁 Absolute path written: {os.path.abspath(output_path)}")
    print(f"📄 File exists after write? {os.path.exists(output_path)}")


if __name__ == "__main__":
    GOLD_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\spacyMapped"
    PRED_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_sm"
    
    OUTPUT_DIR = r"C:\Users\babus\Downloads"
    OUTPUT_FILE = "ner_results_sm.csv"

    evaluate_all_and_save(GOLD_DIR, PRED_DIR, OUTPUT_DIR, OUTPUT_FILE)
    
