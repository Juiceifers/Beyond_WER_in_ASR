import os
import json
from lxml import etree
from tqdm import tqdm

# ========= 🧾 INPUTS ========= #

MEETINGS_ES = ["ES2016a", "ES2016b", "ES2016c", "ES2016d"]

SEGMENT_PATHS_ES = {
    "ES2016a": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\segments\ES2016a.segments.xml",
    "ES2016b": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\segments\ES2016b.segments.xml",
    "ES2016c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\segments\ES2016c.segments.xml",
    "ES2016d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\segments\ES2016d.segments.xml",
}
WORDS_PATHS_ES = {
    "ES2016a": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016a.words.xml",
    "ES2016b": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016b.words.xml",
    "ES2016c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016c.words.xml",
    "ES2016d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016d.words.xml",
}

# for EN2009c-d
MEETINGS_EN = ["EN2009c", "EN2009d"]
SEGMENT_PATHS_EN = {
    "EN2009c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\natural\segments\EN2009c.segments.xml",
    "EN2009d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\natural\segments\EN2009d.segments.xml"
}

WORDS_PATHS_EN = {
    "EN2009c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\natural\words\EN2009c.words.xml",
    "EN2009d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\amicorpus\ami_annotations\merged\natural\words\EN2009d.words.xml"
}

OUTPUT_DIR_EN = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural"
OUTPUT_DIR_ES = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario"

# ========= 🔧 CORE FUNCTIONS ========= #

def parse_segments(path):
    tree = etree.parse(path)
    root = tree.getroot()
    segments = []
    for seg in root.xpath("//segment"):
        seg_id = seg.attrib["{http://nite.sourceforge.net/}id"]
        start = float(seg.attrib["transcriber_start"])
        end = float(seg.attrib["transcriber_end"])
        segments.append({"id": seg_id, "start": start, "end": end})
    return segments

def parse_words(path):
    tree = etree.parse(path)
    root = tree.getroot()
    words = []
    for w in root.xpath("//w"):
        word = w.text
        if word is None or word.strip() == "":
            continue
        start = float(w.attrib["starttime"])
        end = float(w.attrib["endtime"])
        words.append({"word": word.strip(), "start": start, "end": end})
    return words

def align_words_to_segments(segments, words):
    transcripts = []
    for seg in segments:
        seg_start = seg["start"]
        seg_end = seg["end"]
        seg_id = seg["id"]
        seg_words = [
            w["word"]
            for w in words
            if seg_start <= w["start"] < seg_end
        ]
        reference = " ".join(seg_words)
        transcripts.append({
            "segment_id": seg_id,
            "start_time": seg_start,
            "end_time": seg_end,
            "reference": reference
        })
    return transcripts

def generate_gold_transcripts(meetings, seg_paths, word_paths, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for meeting_id in tqdm(meetings, desc=f"Generating gold transcripts in {output_dir}"):
        segments = parse_segments(seg_paths[meeting_id])
        words = parse_words(word_paths[meeting_id])
        aligned = align_words_to_segments(segments, words)

        # Write JSONL: Segment-wise gold references
        jsonl_path = os.path.join(output_dir, f"gold_references_{meeting_id}.jsonl")
        with open(jsonl_path, "w", encoding="utf-8") as outfile:
            for entry in aligned:
                entry["meeting_id"] = meeting_id
                json.dump(entry, outfile)
                outfile.write("\n")

        # Write TXT: Concatenated full gold reference
        full_text = "\n".join(entry["reference"] for entry in aligned if entry["reference"].strip())
        txt_path = os.path.join(output_dir, f"{meeting_id}.gold.txt")
        with open(txt_path, "w", encoding="utf-8") as txtfile:
            txtfile.write(full_text)

    print(f"✅ Done! JSONL and TXT files saved in: {output_dir}")

# ========= 🚀 RUN ========= #

generate_gold_transcripts(MEETINGS_ES, SEGMENT_PATHS_ES, WORDS_PATHS_ES, OUTPUT_DIR_ES)
generate_gold_transcripts(MEETINGS_EN, SEGMENT_PATHS_EN, WORDS_PATHS_EN, OUTPUT_DIR_EN)
