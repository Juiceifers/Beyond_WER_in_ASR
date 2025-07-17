# Beyond WER in ASR: Evaluating Conversational Speech Recognition Systems

This repository contains the code, evaluation scripts, and supporting files for the bachelor thesis **"Exploring Lightweight Metrics for Information Retention in ASR Output Beyond WER"**, focused on evaluating automatic speech recognition (ASR) systems beyond conventional Word Error Rate (WER), using a combination of token- and semantic-level metrics.

The project uses the AMI Meeting Corpus and Whisper-generated transcripts, comparing transcription quality across natural and scenario-based meeting settings while also considering punctuation.

---

## Project Goals

- Evaluate Whisper ASR outputs on **conversational speech**.
- Compare natural vs. scenario-based AMI meetings.
- Assess impact of **punctuation**, **disfluencies**, and **segment length**.
- Analyze metric inter-correlations and statistical significance.
- Demonstrate the limitations of WER and advantages of complementary metrics.

---

## Folder Structure

```plaintext
## 📁 Folder Structure

Beyond-WER-in-ASR/
│
├── data/
│   ├── AMI_manual_annotations/
│   │   ├── merged/
│   │   │   ├── natural/
│   │   │   └── scenario/
│   │   └── original/
│   │       ├── natural/
│   │       ├── scenario/
│   │       └── ne/segments/words/
│   │
│   ├── audio_files/
│   │   ├── natural_meetings/
│   │   ├── scenario_meetings/
│   │   └── testing/
│   │
│   ├── eval_results/
│   │   ├── ...
│   │
│   ├── gold_scripts/
│   │   ├── NER/
│   │   └── transcripts/
│   │
│   └── WHISPER_outputs/
│       ├── natural/
│       ├── scenario/
│       └── test/
│
├── paper/
│   ├── Beyond_WER_in_ASR_paper_v1.pdf
│   └── paper_submission+_guidelines.pdf
│
├── scripts/
│   ├── 1_preprocessing/
│   ├── 2_creating_gold/
│   ├── 3_running whisper/
│   ├── 4_eval_metrics/
│   │   └── testing/
│   ├── 5_NER/
├── requirements.txt
├── .gitattributes
└── README.md
