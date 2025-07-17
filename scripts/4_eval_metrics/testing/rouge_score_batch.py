import os
import csv
import evaluate
rouge = evaluate.load("rouge")


def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def compute_rouge_single_file(ref_path, hyp_path, metric_type="rouge1"):
    gold_text = read_text_file(ref_path)
    hyp_text = read_text_file(hyp_path)
    result = rouge.compute(predictions=[hyp_text], references=[gold_text], use_aggregator=True)
    return round(result[metric_type] * 100, 2)


def compute_rouge_for_directory(gold_dir, hyp_dir, tag, metric_type="rouge1"):
    scores = {}

    for hyp_file in os.listdir(hyp_dir):
        if hyp_file.endswith(".txt"):
            hyp_path = os.path.join(hyp_dir, hyp_file)
            meeting_id = hyp_file.split(".")[0]

            if tag == "disfluencies_removed":
                gold_file = f"{meeting_id}.gold_normalized_normalized_cleaned.txt"
            else:
                gold_file = f"{meeting_id}.gold_normalized.txt"

            gold_path = os.path.join(gold_dir, gold_file)

            if not os.path.isfile(gold_path):
                print(f"⚠️ No gold file for {hyp_file} found in {gold_dir}")
                continue

            score = compute_rouge_single_file(gold_path, hyp_path, metric_type)
            if meeting_id not in scores:
                scores[meeting_id] = {}
            scores[meeting_id][tag] = score
            print(f"✅ {meeting_id} — {tag} {metric_type.upper()}: {score:.2f}")

    return scores

def write_grouped_scores_to_csv(rouge1_scores, rougeL_scores, output_csv_path):
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # ROUGE-1 block
        writer.writerow(["ROUGE-1 F1 Scores"])
        writer.writerow(["File", "with_punct", "without_punct", "disfluencies_removed"])
        for file_name in sorted(rouge1_scores):
            s = rouge1_scores[file_name]
            row = [
                file_name,
                s.get("with_punct", ""),
                s.get("without_punct", ""),
                s.get("disfluencies_removed", "")
            ]
            writer.writerow(row)

        writer.writerow([])  # Empty row

        # ROUGE-L block
        writer.writerow(["ROUGE-L F1 Scores"])
        writer.writerow(["File", "with_punct", "without_punct", "disfluencies_removed"])
        for file_name in sorted(rougeL_scores):
            s = rougeL_scores[file_name]
            row = [
                file_name,
                s.get("with_punct", ""),
                s.get("without_punct", ""),
                s.get("disfluencies_removed", "")
            ]
            writer.writerow(row)

if __name__ == "__main__":
    output_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\eval_results\ROUGE_scores.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Define scenario directories
    # order: tag, gold, whisper
    scenario_dirs = {
        "with_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\normalized_p",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized_p"
        ),
        "without_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\normalized",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized"
        ),
        "disfluencies_removed": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\cleaned",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\cleaned"
        )
    }

    # Define natural directories
    natural_dirs = {
        "with_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\normalized_p",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\normalized_p"
        ),
        "without_punct": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\normalized",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\normalized"
        ),
        "disfluencies_removed": (
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\cleaned",
            r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\cleaned"
        )
    }

    rouge1_scores = {}
    rougeL_scores = {}

    for tag, (gold_dir, hyp_dir) in scenario_dirs.items():
        r1 = compute_rouge_for_directory(gold_dir, hyp_dir, tag, metric_type="rouge1")
        rl = compute_rouge_for_directory(gold_dir, hyp_dir, tag, metric_type="rougeL")
        for k, v in r1.items():
            rouge1_scores.setdefault(k, {}).update(v)
        for k, v in rl.items():
            rougeL_scores.setdefault(k, {}).update(v)

    for tag, (gold_dir, hyp_dir) in natural_dirs.items():
        r1 = compute_rouge_for_directory(gold_dir, hyp_dir, tag, metric_type="rouge1")
        rl = compute_rouge_for_directory(gold_dir, hyp_dir, tag, metric_type="rougeL")
        for k, v in r1.items():
            rouge1_scores.setdefault(k, {}).update(v)
        for k, v in rl.items():
            rougeL_scores.setdefault(k, {}).update(v)

    write_grouped_scores_to_csv(rouge1_scores, rougeL_scores, output_path)
