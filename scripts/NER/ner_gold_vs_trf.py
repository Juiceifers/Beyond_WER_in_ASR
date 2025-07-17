import os
import re
import csv



def extract_meeting_id(filename):
    """Extracts meeting ID like ES2016a from any known filename pattern."""
    match = re.search(r'(ES2016[abcd])', filename)
    return match.group(1) if match else None

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

def compare_ner_entities(gold_path, trf_path, label, output_dir, csv_writer):
    gold_entities = load_ner_entities(gold_path)
    trf_entities = load_ner_entities(trf_path)

    only_in_gold = gold_entities - trf_entities
    only_in_trf = trf_entities - gold_entities
    common = gold_entities & trf_entities

    os.makedirs(output_dir, exist_ok=True)
    output_txt = os.path.join(output_dir, f"{label}_ner_comparison.txt")

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"📂 Comparing: {label} (TRF vs GOLD)\n\n")

        f.write(f"✅ In GOLD but not in TRF ({len(only_in_gold)}):\n")
        for span, lbl in sorted(only_in_gold):
            f.write(f"  {span} -> [{lbl}]\n")

        f.write(f"\n❌ In TRF but not in GOLD ({len(only_in_trf)}):\n")
        for span, lbl in sorted(only_in_trf):
            f.write(f"  {span} -> [{lbl}]\n")

        f.write(f"\n📊 Summary for {label}:\n")
        f.write(f"  Total GOLD entities: {len(gold_entities)}\n")
        f.write(f"  Total TRF entities:  {len(trf_entities)}\n")
        f.write(f"  Matching entities:   {len(common)}\n")
        f.write(f"  Total mismatches:    {len(only_in_gold | only_in_trf)}\n")

    match_score = (2 * len(common)) / (len(gold_entities) + len(trf_entities)) * 100 if (gold_entities or trf_entities) else 0

    csv_writer.writerow({
        'Meeting': label,
        'GOLD total': len(gold_entities),
        'TRF total': len(trf_entities),
        'Matching': len(common),
        'Only in GOLD': len(only_in_gold),
        'Only in TRF': len(only_in_trf),
        'Total mismatches': len(only_in_gold | only_in_trf),
        'Match %': round(match_score, 2)
    })


if __name__ == "__main__":
    GOLD_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER\spacyMapped"        
    TRF_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_trf"    
    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\eval_results\NER\spacy_comparison_reports\trf_vs_gold"
    SUMMARY_CSV = os.path.join(OUTPUT_DIR, "trf_vs_gold_summary.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Match by filename prefix
    gold_files = {}
    for f in os.listdir(GOLD_DIR):
        if f.endswith(".txt"):
            meeting_id = extract_meeting_id(f)
            if meeting_id:
                gold_files[meeting_id] = os.path.join(GOLD_DIR, f)

    trf_files = {}
    for f in os.listdir(TRF_DIR):
        if f.endswith("_rf.txt"):
            meeting_id = extract_meeting_id(f)
            if meeting_id:
                trf_files[meeting_id] = os.path.join(TRF_DIR, f)


    common_keys = sorted(set(gold_files.keys()) & set(trf_files.keys()))

    with open(SUMMARY_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Meeting', 'GOLD total', 'TRF total', 'Matching', 'Only in GOLD', 'Only in TRF', 'Total mismatches', 'Match %']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key in common_keys:
            gold_path = gold_files[key]
            trf_path = trf_files[key]
            compare_ner_entities(gold_path, trf_path, label=key, output_dir=OUTPUT_DIR, csv_writer=writer)

    print(f"\n📄 Summary CSV saved to: {SUMMARY_CSV}\n")
