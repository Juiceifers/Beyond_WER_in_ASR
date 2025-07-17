import os
import json
from lxml import etree
from tqdm import tqdm


def load_ne_type_mapping(ne_types_path):
    tree = etree.parse(ne_types_path)
    root = tree.getroot()
    mapping = {}
    for ne_type in root.xpath(".//ne-type"):
        xml_id = ne_type.attrib.get("{http://nite.sourceforge.net/}id")
        name = ne_type.attrib.get("name")
        if xml_id and name:
            mapping[xml_id] = name
    return mapping



def parse_words_with_ids(path):
    tree = etree.parse(path)
    word_map = {}
    for w in tree.xpath("//w"):
        wid = w.attrib.get("{http://nite.sourceforge.net/}id")
        text = w.text.strip() if w.text else ""
        if wid and text:
            word_map[wid] = text
    return word_map


def parse_ner_annotations(path, ne_mapping):
    ns = {"nite": "http://nite.sourceforge.net/"}
    tree = etree.parse(path)
    root = tree.getroot()
    entities = []

    for entity in root.xpath("//named-entity", namespaces=ns):
        pointer = entity.find("nite:pointer", namespaces=ns)
        if pointer is None or "href" not in pointer.attrib:
            continue
        href = pointer.attrib["href"]
        label_id = href.split("#id(")[-1].rstrip(")")
        label = ne_mapping.get(label_id, label_id)  # fallback to raw ID if label missing

        child = entity.find("nite:child", namespaces=ns)
        if child is None or "href" not in child.attrib:
            continue
        span = child.attrib["href"]

        try:
            span = span.split("#id(")[-1].rstrip(")")
            if "..id(" in span:
                start_id, end_id = span.split(")..id(")
            else:
                start_id = end_id = span
        except Exception:
            continue

        entities.append({
            "start": start_id,
            "end": end_id,
            "label": label
        })

    return entities


def resolve_entities(word_map, entities):
    resolved = []
    word_ids = list(word_map.keys())
    for entity in entities:
        start_id = entity["start"]
        end_id = entity["end"]

        if start_id not in word_ids or end_id not in word_ids:
            continue

        start_idx = word_ids.index(start_id)
        end_idx = word_ids.index(end_id)
        span_words = [word_map[word_ids[i]] for i in range(start_idx, end_idx + 1)]
        entity_text = " ".join(span_words)
        resolved.append({
            "start_id": start_id,
            "end_id": end_id,
            "label": entity["label"],
            "text": entity_text
        })
    return resolved


def generate_ner_gold_transcripts(meetings, word_paths, ne_paths, ne_type_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ne_mapping = load_ne_type_mapping(ne_type_path)

    for meeting_id in tqdm(meetings, desc="Generating NER gold transcripts"):
        word_map = parse_words_with_ids(word_paths[meeting_id])
        entities = parse_ner_annotations(ne_paths[meeting_id], ne_mapping)
        resolved_entities = resolve_entities(word_map, entities)

        jsonl_path = os.path.join(output_dir, f"ner_gold_{meeting_id}.jsonl")
        with open(jsonl_path, "w", encoding="utf-8") as outfile:
            for entity in resolved_entities:
                entity["meeting_id"] = meeting_id
                json.dump(entity, outfile)
                outfile.write("\n")

        txt_path = os.path.join(output_dir, f"{meeting_id}.ner.gold.txt")
        with open(txt_path, "w", encoding="utf-8") as txtfile:
            for entity in resolved_entities:
                txtfile.write(f"{entity['text']} -> [{entity['label']}]\n")

    print(f"\n✅ All files saved in: {output_dir}\n")



if __name__ == "__main__":
    MEETINGS = ["ES2016a", "ES2016b", "ES2016c", "ES2016d"]

    WORDS_PATHS = {
        "ES2016a": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016a.words.xml",
        "ES2016b": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016b.words.xml",
        "ES2016c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016c.words.xml",
        "ES2016d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words\ES2016d.words.xml"
    }

    NE_PATHS = {
        "ES2016a": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner\ES2016a.ne.xml",
        "ES2016b": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner\ES2016b.ne.xml",
        "ES2016c": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner\ES2016c.ne.xml",
        "ES2016d": r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner\ES2016d.ne.xml"
    }

    OUTPUT_DIR = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\NER"
    NE_TYPES_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner\ne-types.xml"
    
    generate_ner_gold_transcripts(MEETINGS, WORDS_PATHS, NE_PATHS, NE_TYPES_PATH, OUTPUT_DIR)
