import sacrebleu
import os

def read_text_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def compute_bleu_single_file(ref_path, hyp_path):
    # Read both files
    gold_text = read_text_file(ref_path)
    whisper_text = read_text_file(hyp_path)

    # Compute BLEU
    bleu = sacrebleu.corpus_bleu([whisper_text], [[gold_text]])
    print(f"✅ BLEU score: {bleu.score:.2f}")
    return bleu.score

def write_score_to_file(score, output_path, tag):
    with open(output_path, 'a', encoding='utf-8') as f:  # 'a' = append mode
        if tag =="without_punct":
            f.write(f"BLEUE Score when punctuations REMOVED:\t{score:.2f}\n")
        else:
            f.write(f"BLEUE Score when punctuation KEPT:\t\t{score:.2f}\n")
    print(f"📁 Score appended to: {output_path}")


if __name__ == "__main__":
    # === SET YOUR FILE PATHS HERE ===
    gold_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\normalized\ES2016a.gold_normalized.txt"
    whisper_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized\ES2016a.Mix-Headset_normalized.txt"
    output_path = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\eval_results\Test\BLEUE_ES2016a.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    score = compute_bleu_single_file(gold_path, whisper_path)
    write_score_to_file(score, output_path, "without_punct")

    gold_path_p = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\normalized\normalized_p\ES2016a.gold_normalized.txt"
    whisper_path_p = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized\normalized_p\ES2016a.Mix-Headset_normalized.txt"

    score_p = compute_bleu_single_file(gold_path_p, whisper_path_p)
    write_score_to_file(score_p, output_path, "with_punct")
