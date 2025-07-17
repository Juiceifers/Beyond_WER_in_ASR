import json
import os

def calculate_total_duration(jsonl_path, output_txt_path):
    total_duration = 0.0

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            record = json.loads(line)
            start = record.get("start_time")
            end = record.get("end_time")
            if start is not None and end is not None:
                total_duration += (end - start)

    # Format time
    h = int(total_duration // 3600)
    m = int((total_duration % 3600) // 60)
    s = int(total_duration % 60)
    formatted = f"Total duration: {h}h {m}m {s}s ({total_duration:.2f} seconds)"

    # Write to file
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    with open(output_txt_path, 'w', encoding='utf-8') as out:
        out.write(formatted + "\n")

    print(f"✅ Duration written to: {output_txt_path}")
    return total_duration


if __name__ == "__main__":
    BASE_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\gold"
    tag = "natural"
    output_txt = os.path.join(BASE_PATH,tag, "total_duration")

    # MEETINGS = ["ES2016a_gold", "ES2016b_gold", "ES2016c_gold", "ES2016d_gold"]
    # input_files_path = {
    #     "ES2016a_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\gold\gold_references_ES2016a.jsonl",
    #     "ES2016b_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\gold\gold_references_ES2016b.jsonl",
    #     "ES2016c_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\gold\gold_references_ES2016c.jsonl",
    #     "ES2016d_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\gold\gold_references_ES2016d.jsonl",
    #     }
    MEETINGS = ["EN2009c_gold", "EN2009d_gold"]
    input_files_path = {
        "EN2009c_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\gold\natural\gold_references_EN2009c.jsonl",
        "EN2009d_gold": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\gold\natural\gold_references_EN2009d.jsonl",
        }
    total_duration = 0
    per_meeting_durations = {}
    
    for meeting_id in MEETINGS:
        dur = calculate_total_duration(input_files_path[meeting_id], output_txt)
        total_duration += dur
        per_meeting_durations[meeting_id] = dur

    with open(output_txt, "w", encoding="utf-8") as out:
        for meeting_id, dur in per_meeting_durations.items():
            h = int(dur // 3600)
            m = int((dur % 3600) // 60)
            s = int(dur % 60)
            out.write(f"{meeting_id}: {h}h {m}m {s}s ({dur:.2f} seconds)\n")
        h = int(total_duration // 3600)
        m = int((total_duration % 3600) // 60)
        s = int(total_duration % 60)
        out.write(f"\nTotal duration:: {h}h {m}m {s}s ({total_duration:.2f} seconds)\n")
