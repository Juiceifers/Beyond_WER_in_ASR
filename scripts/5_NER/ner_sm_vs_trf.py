import os
import re
import csv

def load_ner_entities(file_path):
    """Loads lines like: Nick Debusk -> [PERSON] into (text, label) tuples."""
    entities = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '->' not in line:
                continue
            try:
                span, label_part = line.split('->')
                span = span.strip()
                label = re.sub(r'[\[\]\s]', '', label_part.strip())
                entities.add((span, label))
            except ValueError:
                continue
    return entities

def compare_ner_entities(sm_path, trf_path, label, output_dir, csv_writer):
    sm_entities = load_ner_entities(sm_path)
    trf_entities = load_ner_entities(trf_path)

    only_in_sm = sm_entities - trf_entities
    only_in_trf = trf_entities - sm_entities
    common = sm_entities & trf_entities

    os.makedirs(output_dir, exist_ok=True)
    output_txt = os.path.join(output_dir, f"{label}_ner_comparison.txt")

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"📂 Comparing: {label}\n\n")
        f.write(f"✅ In SM but not TRF ({len(only_in_sm)}):\n")
        for span, lbl in sorted(only_in_sm):
            f.write(f"  {span} -> [{lbl}]\n")

        f.write(f"\n❌ In TRF but not SM ({len(only_in_trf)}):\n")
        for span, lbl in sorted(only_in_trf):
            f.write(f"  {span} -> [{lbl}]\n")

        f.write(f"\n📊 Summary for {label}:\n")
        f.write(f"  Total SM entities:  {len(sm_entities)}\n")
        f.write(f"  Total TRF entities: {len(trf_entities)}\n")
        f.write(f"  Matching entities:  {len(common)}\n")
        f.write(f"  Total mismatches:   {len(only_in_sm | only_in_trf)}\n")

    match_score = (2 * len(common)) / (len(sm_entities) + len(trf_entities)) * 100 if (sm_entities or trf_entities) else 0

    csv_writer.writerow({
        'Meeting': label,
        'SM total': len(sm_entities),
        'TRF total': len(trf_entities),
        'Matching': len(common),
        'Only in SM': len(only_in_sm),
        'Only in TRF': len(only_in_trf),
        'Total mismatches': len(only_in_sm | only_in_trf),
        'Match %': round(match_score, 2)
    })



if __name__ == "__main__":
    BASE = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy"
    SM_DIR = os.path.join(BASE, "spacy_sm")
    TRF_DIR = os.path.join(BASE, "spacy_trf")
    OUTPUT_DIR = os.path.join(BASE, "comparison_reports")
    SUMMARY_CSV = os.path.join(OUTPUT_DIR, "ner_comparison_summary.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Automatically find matching files by shared prefix
    sm_files = {f.replace("_sm.txt", ""): os.path.join(SM_DIR, f) for f in os.listdir(SM_DIR) if f.endswith("_sm.txt")}
    trf_files = {f.replace("_rf.txt", ""): os.path.join(TRF_DIR, f) for f in os.listdir(TRF_DIR) if f.endswith("_rf.txt")}

    # Find shared base names
    common_keys = sorted(set(sm_files.keys()) & set(trf_files.keys()))

    with open(SUMMARY_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Meeting', 'SM total', 'TRF total', 'Matching', 'Only in SM', 'Only in TRF', 'Total mismatches', 'Match %']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key in common_keys:
            sm_path = sm_files[key]
            trf_path = trf_files[key]
            compare_ner_entities(sm_path, trf_path, label=key, output_dir=OUTPUT_DIR, csv_writer=writer)

    print(f"\n📄 Summary CSV saved to: {SUMMARY_CSV}\n")
