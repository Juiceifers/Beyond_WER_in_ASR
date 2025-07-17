import os
import re

# Define common disfluencies
DISFLUENCIES = {"uh", "um", "uhm", "mm", "mm-hmm", "huh"}


def remove_disfluencies(text):
    # Lowercase for consistent matching
    text = text.lower()
    
    for pattern in DISFLUENCIES:
        text = re.sub(pattern, '', text)

    # Clean leftover whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_transcription_dir(input_dir, output_dir):
    cleaned_dir = os.path.join(output_dir, "cleaned")
    os.makedirs(cleaned_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.endswith(".txt"):
            input_path = os.path.join(input_dir, fname)
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()

            cleaned_text = remove_disfluencies(text)

            base, ext = os.path.splitext(fname)
            output_path = os.path.join(cleaned_dir, base + "_normalized_cleaned" + ext)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text + "\n")

            print(f"✅ Cleaned: {fname} → {os.path.basename(output_path)}")
            
  
if __name__ == "__main__":
    gold_scen_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario\normalized"         
    gold_scen_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\scenario"  
    clean_transcription_dir(gold_scen_input_dir, gold_scen_output_dir)

    gold_nat_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural\normalized"         
    gold_nat_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\gold_scripts\transcripts\natural"  
    clean_transcription_dir(gold_nat_input_dir, gold_nat_output_dir)

    whisper_scen_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\normalized"         
    whisper_scen_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario"  
    clean_transcription_dir(whisper_scen_input_dir, whisper_scen_output_dir)

    whisper_nat_input_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural\normalized"         
    whisper_nat_output_dir = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\natural"  
    clean_transcription_dir(whisper_nat_input_dir, whisper_nat_output_dir)
