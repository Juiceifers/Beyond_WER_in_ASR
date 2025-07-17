import os
import glob
import xml.etree.ElementTree as ET
from collections import defaultdict

def merge_by_meeting(input_dir, output_dir, tag, file_suffix=".xml", namespace=None):
    """
    Merges multiple AMI XML files per meeting into one.

    Parameters:
    - input_dir: folder containing speaker-level XML files
    - output_dir: where to save merged files
    - tag: the XML root tag to create (e.g., 'words', 'segments', 'ne')
    - file_suffix: expected suffix (default: .xml)
    - namespace: optional namespace to include in the root tag (for e.g., NITE files)
    """
    os.makedirs(output_dir, exist_ok=True)
    all_files = glob.glob(os.path.join(input_dir, f"*.{tag}*{file_suffix}"))
    print(f"🔍 Found {len(all_files)} files in {input_dir}")
    if not all_files:
        print("❌ No files found! Check path and extension.")
        return
    print("Files:", [os.path.basename(f) for f in all_files])

    meeting_groups = defaultdict(list)
    for filepath in all_files:
        filename = os.path.basename(filepath)
        meeting_id = filename.split(".")[0]
        meeting_groups[meeting_id].append(filepath)

    for meeting_id, filepaths in meeting_groups.items():
        print(f"\n🔧 Merging files for meeting: {meeting_id}")
        
        # Create root element, adding namespace if needed
        if namespace:
            ET.register_namespace('nite', namespace)
            root = ET.Element(f"{{{namespace}}}root", {f"{{{namespace}}}id": f"{meeting_id}.{tag}"})
        else:
            root = ET.Element(tag)

        for file in filepaths:
            try:
                tree = ET.parse(file)
                for child in tree.getroot():
                    root.append(child)
            except Exception as e:
                print(f"❌ Error parsing {file}: {e}")

        merged_tree = ET.ElementTree(root)
        output_filename = f"{meeting_id}.{tag}.xml"
        output_path = os.path.join(output_dir, output_filename)
        merged_tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"✅ Saved merged file: {output_path}")

if __name__ == "__main__":
    # for word files NATURAL
    w_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\original\natural\words"
    w_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\natural\words"
    merge_by_meeting(w_input_dir, w_output_dir, "words")
    # for word files SCENARIO
    w_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\original\scenario\words"
    w_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\words"
    merge_by_meeting(w_input_dir, w_output_dir, "words")


    # for segment files NATURAL
    s_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\original\natural\segments"
    s_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\natural\segments"
    merge_by_meeting(s_input_dir, s_output_dir, "segments")

    # for segment files SCENARIO
    s_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\original\scenario\segments"
    s_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\segments"
    merge_by_meeting(s_input_dir, s_output_dir, "segments")


    # for NE SCENARIO
    ne_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\original\scenario\ne"
    ne_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\manual_annotations\merged\scenario\ner"
    merge_by_meeting(ne_input_dir, ne_output_dir, "ne", namespace="http://nite.sourceforge.net/")

    