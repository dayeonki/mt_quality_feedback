# Should I Share this Translation? Evaluating Quality Feedback for User Reliance on Machine Translation

Authors: Dayeon Ki, Kevin Duh, Marine Carpuat

This repository contains the code and dataset for our EMNLP 2025 Main paper **Should I Share this Translation? Evaluating Quality Feedback for User Reliance on Machine Translation**.

<div align="center">
<img src="https://github.com/user-attachments/assets/b3415a65-ccac-4468-a291-07602cb95509" style="width: 15px;" alt="code"> <b><a href=https://github.com/dayeonki/mt_quality_feedback>Code</a></b> | 
  <img src="https://github.com/user-attachments/assets/fc2ca3c2-3e78-4ca4-a208-448c0a6c7068" style="width: 15px;" alt="paper"> <b><a href=https://drive.google.com/file/d/1gjhPpiKtAsCau6rFZShUMsJTlCQb4tmu/view?usp=sharing>Paper</a></b>
</div>


## Abstract
In our human study, each English-speaking monolingual participant reviews a sequence of 20 decision-making examples. Each example is shown in a two-step process: **1) Independent decision-making**: Participants first make judgments based solely on the English source and its Spanish MT output and **2) AI-Assisted decision-making**: They then reassess the same example with one of four randomly assigned feedback types. For each step, they respond to two questions: 1) Shareability: To the best of your knowledge, is the Spanish translation good enough to safely share with your Spanish-speaking neighbor? and 2) Confidence: How confident are you in your assessment? The following figure is an illustration of our human study setup.

<p align="center">
  <img src="https://github.com/user-attachments/assets/b37766f5-8fed-44c1-bf18-5eaa6c2c54cc" width="700">
</p>

## Quick Links
- [Quality Feedback Types](#quality-feedback-types)
- [Task Interface](#task-interface)
- [Evaluation](#evaluation)
- [Visualization](#visualization)



## Quality Feedback Types

We explore four types of quality feedback in our human study. Detailed process used to generate each feedback is outlined in the paper.

- **Explicit** quality assessments of MT output
  - Error Highlights
  - LLM Explanation
- **Implicit** assessments to guide participants compare MT input and output
  - Backtranslation
  - QA Table

<p align="center">
  <img src="https://github.com/user-attachments/assets/879ee2ef-4e3c-4381-ba70-423e4a152a4c" width="700">
</p>


## Task Interface

We provide codebase for building our custom task interface in `interface/`. Code is written based on the interface code from EMNLP 2023 paper <a href="https://github.com/Elbria/Ex-SemDiv?tab=readme-ov-file">Explaining with Contrastive Phrasal Highlighting: A Case Study in Assisting Humans to Detect Translation Differences</a>.

Go through the following steps to run the interface:
- `rm -rf tracker`: Removing the tracker directory, which save files to track each condition to ensure each participant is randonly assigned to each of four conditions.
- `mkdir tracker`: Make new directory for the tracker.
- `python create_tracker.py`: Run the code to create tracker for each condition.
- `python -u app.py > app.log`: Run the `app.py` file and log results to `app.log` file.

<p align="center">
  <img src="https://github.com/user-attachments/assets/3854b2d9-c71e-4b2a-bd84-3397dc8b0bf2" width="700">
</p>


## Evaluation

We measure three dependent variables in our paper: (1) Decision accuracy, (2) CWA (Confidence-Weighted Accuracy), and (3) Switch percentage.

- **Decision accuracy** is measured by comparing each participant's shareability judgment against the gold label for each example for all examples.
- **CWA** is measured by combining the decision accuracy and confidence scores using confidence weighting to evaluate whether participants made the correct decision weighted by their confidence in that decision. This metric serves as a measure of (in)appropriate reliance, where higher scores indicate accurate decisions made with well-calibrated confidence.
- **Switch percentage** is a widely used behavioral measure of reliance, capturing how often participants change their decisions after viewing AI feedback. In our context, it reflects how quality feedback influences final shareability judgments. We compute three metrics:
  - Over-reliance: the proportion of cases where a participant changes from a correct to an incorrect decision after feedback
  - Under-reliance: the proportion of cases where a participant does not change from an incorrect decision to a correct one after the quality feedback
  - Appropriate reliance: the proportion of cases where a participant either corrects an incorrect decision after receiving feedback (switch) or maintains a correct decision (no switch)


From the collected responses, we evaluate the following:
- `evaluation/make_summary.py`: Make a summary csv file from the raw responses for analysis. This code will generate `summary.csv` file, which will be used for further evaluation below.
- `evaluation/dv_summary.py`: Calculate each dependent variable (decision accuracy and CWA).
- `evaluation/bonus_tracker.py`: Track for participants who will receive performance-based bonus (over 70% overall accuracy).
- `evaluation/free_comments.py`: Analyze participants' free-form responses.
- `evaluation/post_survey_analysis.py`: Analyze participants' post-task survey questions on perceived helpfulness, trust in future use, and mental burden.
- `evaluation/switch_percentage.py`: Calculate breakdown of switch percentage.


We further test **statistical significance** for each dependent variable:
- `evaluation/significance_test/between_ind.py`: Significance test between each independent decision-making performance across conditions.
- `evaluation/significance_test/between_ai.py`: Significance test between each AI-assisted decision-making performance across conditions.
- `evaluation/significance_test/within.py`: Significance test within each condition (Independent vs. AI-assisted).
- `evaluation/significance_test/per_label.py`: Significance test per shareability label (Safe to share as-is, Needs bilingual review before sharing).



## Visualization

We release our code used for creating visualizations in the paper:

(1) `visualization/main_evaluation.py`

<p align="center">
  <img src="https://github.com/user-attachments/assets/4fd6d845-6eef-4e7b-82be-b5be8b18a361" width="700">
</p>

(2) `visualization/per_shareability.py`

<p align="center">
  <img src="https://github.com/user-attachments/assets/756e493a-98f4-45ef-9d24-def93822409d" width="700">
</p>

(3) `visualization/switch_percentage.py`

<p align="center">
  <img src="https://github.com/user-attachments/assets/89dcf83d-62a7-4ffb-8f0a-1343eef8c75f" width="400">
</p>
