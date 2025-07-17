import os
import json
from lxml import etree
from tqdm import tqdm

#for ES2016a-d
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

# SCENARIO
for meeting_id in tqdm(MEETINGS_ES):
    segments = parse_segments(SEGMENT_PATHS_ES[meeting_id])
    words = parse_words(WORDS_PATHS_ES[meeting_id])
    aligned = align_words_to_segments(segments, words)

    output_path = os.path.join(OUTPUT_DIR_ES, f"gold_references_{meeting_id}.jsonl")
    with open(output_path, "w", encoding="utf-8") as outfile:
        for entry in aligned:
            entry["meeting_id"] = meeting_id
            json.dump(entry, outfile)
            outfile.write("\n")

print(f"\n✅ Done! Gold references saved to: {OUTPUT_DIR_ES}\\gold_references_<meeting_id>.jsonl")

# NATURAL
for meeting_id in tqdm(MEETINGS_EN):
    segments = parse_segments(SEGMENT_PATHS_EN[meeting_id])
    words = parse_words(WORDS_PATHS_EN[meeting_id])
    aligned = align_words_to_segments(segments, words)

    output_path = os.path.join(OUTPUT_DIR_EN, f"gold_references_{meeting_id}.jsonl")
    with open(output_path, "w", encoding="utf-8") as outfile:
        for entry in aligned:
            entry["meeting_id"] = meeting_id
            json.dump(entry, outfile)
            outfile.write("\n")

    

print(f"\n✅ Done! Gold references saved to: {OUTPUT_DIR_EN}\\gold_references_<meeting_id>.jsonl")