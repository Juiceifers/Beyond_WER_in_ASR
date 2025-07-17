def compare_ner_tags(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines() #sm
        lines2 = f2.readlines() #trf

    len1, len2 = len(lines1), len(lines2)
    
    if len1 != len2:
        print("❗ Warning: Files have different number of lines!")
        print(f"   sm:  {len1} lines")
        print(f"   trf: {len2} lines")

    min_len = min(len1, len2)
    mismatch_count = 0
    
    print(f"{'Line':<6} {'Token':<15} {'SM':<15} {'TRF':<15}")
    print("-" * 55)
    for i in range(min_len):
        token1, tag1 = lines1[i].strip().split('\t')
        token2, tag2 = lines2[i].strip().split('\t')

        if tag1 != tag2:
            mismatch_count += 1
            print(f"{str(i+1):<6} {token1:<15} {tag1:<15} {tag2:<15}")

    print(f"\nTotal mismatches: {mismatch_count} out of {min_len} compared lines.")

    if len1 != len2:
        print("Only the first", min_len, "lines were compared due to unequal lengths.\n")


if __name__ == "__main__":
    print(f"Comparing ES2016a")
    SM_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_sm\ES2016a.Mix-Headset.iob.txt"
    TRF_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_trf\ES2016a.Mix-Headset.iob.txt"
    compare_ner_tags(SM_PATH, TRF_PATH)

    print(f"\nComparing ES2016b")
    SM_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_sm\ES2016b.Mix-Headset.iob.txt"
    TRF_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_trf\ES2016b.Mix-Headset.iob.txt"
    compare_ner_tags(SM_PATH, TRF_PATH)

    print(f"\nComparing ES2016a")
    SM_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_sm\ES2016c.Mix-Headset.iob.txt"
    TRF_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_trf\ES2016c.Mix-Headset.iob.txt"
    compare_ner_tags(SM_PATH, TRF_PATH)

    print(f"\nComparing ES2016a")
    SM_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_sm\ES2016d.Mix-Headset.iob.txt"
    TRF_PATH = r"C:\Users\babus\OneDrive\Documents\uni uzh\FS25\conversational speech processing\mypaper\Beyond-WER-in-ASR\data\WHISPER_outputs\scenario\NER\spacy\spacy_trf\ES2016d.Mix-Headset.iob.txt"
    compare_ner_tags(SM_PATH, TRF_PATH)
