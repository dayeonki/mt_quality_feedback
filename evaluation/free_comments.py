import pandas as pd
import glob
import os


csv_dir = 'responses/'
csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

condition_comments = {}

for file in csv_files:
    df = pd.read_csv(file)

    condition = df[df['id'] != 'POSTSURVEY']['condition'].dropna().iloc[0] if 'condition' in df.columns else 'unknown'
    postsurvey_row = df[df['id'] == 'POSTSURVEY']
    if not postsurvey_row.empty:
        row = postsurvey_row.iloc[0]

        for col in ['follow_up_12', 'follow_up_3', 'follow_up_45']:
            comment = str(row.get(col, '')).strip()
            if comment and comment.lower() != 'nan':
                condition_comments.setdefault(condition, {}).setdefault(col, []).append(comment)

for condition, followups in condition_comments.items():
    print(f"\n=== Condition: {condition} ===")
    for question, comments in followups.items():
        print(f"\n{question}:")
        for comment in comments:
            print(f"  • {comment}")
