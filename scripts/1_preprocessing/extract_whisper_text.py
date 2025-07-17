import json
import os

def extract_text_from_whisper(json_path, output_txt_path):
    with open(json_path, "r", encoding="utf-8") as f:
        whisper_data = json.load(f)
    
    text = whisper_data.get("text", "").strip()

    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    with open(output_txt_path, "w", encoding="utf-8") as out:
        out.write(text)

    print(f"✅ Extracted text saved to: {output_txt_path}")

# Example usage — set your paths
json_input = r"C:\Users\babus\Downloads\ES2016a_half.Mix-Headset.json"
txt_output = r"C:\Users\babus\Downloads\ES2016a_half.hyp.txt"

extract_text_from_whisper(json_input, txt_output)
