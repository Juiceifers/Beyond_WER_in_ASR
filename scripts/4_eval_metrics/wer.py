import os
import csv
import jiwer

def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def compute_wer_single_file(ref_path, hyp_path):
    gold = read_text_file(ref_path)
    hyp = read_text_file(hyp_path)
    wer = jiwer.wer(gold, hyp)
    return round(wer * 100, 2)

def compute_wer_for_directory(gold_dir, hyp_dir, tag):
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

            score = compute_wer_single_file(gold_path, hyp_path)
            if meeting_id not in scores:
                scores[meeting_id] = {}
            scores[meeting_id][tag] = score
            print(f"✅ {meeting_id} — {tag} WER: {score:.2f}")

    return scores

def write_wer_scores_to_csv(wer_scores, output_csv_path):
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["WER Scores"])
        writer.writerow(["File", "with_punct", "without_punct"])
        for file_name in sorted(wer_scores):
            s = wer_scores[file_name]
            row = [
                file_name,
                s.get("with_punct", ""),
                s.get("without_punct", "")
            ]
            writer.writerow(row)

if __name__ == "__main__":
    output_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\eval_results\WER_scores.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Scenario directories
    # order: tag, gold, whisper
    scenario_dirs = {
        "with_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\FULLY_NORMALIZED\normalized_p",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\FULLY_NORMALIZED\normalized_p"
        ),
        "without_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\FULLY_NORMALIZED",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\FULLY_NORMALIZED"
        )
    }

    # Natural directories
    natural_dirs = {
        "with_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\FULLY_NORMALIZED\normalized_p",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\FULLY_NORMALIZED\normalized_p"
        ),
        "without_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\FULLY_NORMALIZED",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\FULLY_NORMALIZED"
        )
    }

    wer_scores = {}

    for tag, (gold_dir, hyp_dir) in scenario_dirs.items():
        scores = compute_wer_for_directory(gold_dir, hyp_dir, tag)
        for k, v in scores.items():
            wer_scores.setdefault(k, {}).update(v)

    for tag, (gold_dir, hyp_dir) in natural_dirs.items():
        scores = compute_wer_for_directory(gold_dir, hyp_dir, tag)
        for k, v in scores.items():
            wer_scores.setdefault(k, {}).update(v)

    write_wer_scores_to_csv(wer_scores, output_path)
