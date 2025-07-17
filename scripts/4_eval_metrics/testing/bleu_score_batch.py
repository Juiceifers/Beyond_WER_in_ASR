import sacrebleu
import os
import csv

def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def compute_bleu_single_file(ref_path, hyp_path):
    gold_text = read_text_file(ref_path)
    whisper_text = read_text_file(hyp_path)
    bleu = sacrebleu.corpus_bleu([whisper_text], [[gold_text]])
    return bleu.score

def compute_bleu_for_directory(gold_dir, hyp_dir, tag):
    scores = {}

    for hyp_file in os.listdir(hyp_dir):
        if hyp_file.endswith(".txt"):
            hyp_path = os.path.join(hyp_dir, hyp_file)
            meeting_id = hyp_file.split(".")[0]
            gold_file = f"{meeting_id}.gold_normalized.txt"
            gold_path = os.path.join(gold_dir, gold_file)

            if not os.path.isfile(gold_path):
                print(f"⚠️ No gold file for {hyp_file} found in {gold_dir}")
                continue

            score = compute_bleu_single_file(gold_path, hyp_path)
            if meeting_id not in scores:
                scores[meeting_id] = {}
            scores[meeting_id][tag] = round(score, 2)
            print(f"✅ {meeting_id} — {tag} BLEU: {score:.2f}")

    return scores

def write_scores_to_csv(all_scores, output_csv_path):
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["File", "with_punct", "without_punct"])

        for file_name in sorted(all_scores):
            scores = all_scores[file_name]
            row = [
                file_name,
                scores.get("with_punct", ""),
                scores.get("without_punct", "")
            ]
            writer.writerow(row)

if __name__ == "__main__":
    output_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\eval_results\BLEUE_scores.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_scores = {}

    # SCENARIO
    scen_scores_with = compute_bleu_for_directory(
        gold_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\FULLY_NORMALIZED\normalized_p",
        hyp_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\FULLY_NORMALIZED\normalized_p",
        tag="with_punct"
    )
    scen_scores_wo = compute_bleu_for_directory(
        gold_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\FULLY_NORMALIZED",
        hyp_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\FULLY_NORMALIZED",
        tag="without_punct"
    )

    for d in [scen_scores_with, scen_scores_wo]:
        for file, val in d.items():
            all_scores.setdefault(file, {}).update(val)

    # NATURAL
    nat_scores_with = compute_bleu_for_directory(
        gold_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\FULLY_NORMALIZED\normalized_p",
        hyp_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\FULLY_NORMALIZED\normalized_p",
        tag="with_punct"
    )
    nat_scores_wo = compute_bleu_for_directory(
        gold_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\FULLY_NORMALIZED",
        hyp_dir=r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\FULLY_NORMALIZED",
        tag="without_punct"
    )

    for d in [nat_scores_with, nat_scores_wo]:
        for file, val in d.items():
            all_scores.setdefault(file, {}).update(val)

    write_scores_to_csv(all_scores, output_path)
