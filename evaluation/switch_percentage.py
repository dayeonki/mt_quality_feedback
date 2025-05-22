import pandas as pd
import glob
import os


def calculate_switch_breakdown(df):
    df = df[~df['id'].astype(str).str.endswith('_attn')]
    df = df[df['id'] != 'POSTSURVEY']
    df = df[df['step'].isin([1, 2])]
    df = df.dropna(subset=['id', 'step'])

    df = df.sort_values('timestamp').drop_duplicates(subset=['id', 'step'], keep='last')

    pivot_resp = df.pivot(index='id', columns='step', values='shareability_response')
    pivot_truth = df.pivot(index='id', columns='step', values='is_shareable')

    pivot_resp.columns = ['resp_step_1', 'resp_step_2']
    pivot_truth.columns = ['truth_step_1', 'truth_step_2']
    merged = pivot_resp.join(pivot_truth)
    merged = merged.dropna(subset=['resp_step_1', 'resp_step_2', 'truth_step_1'])


    def classify(row):
        r1, r2 = row['resp_step_1'], row['resp_step_2']
        gt = row['truth_step_1']

        correct_r1 = (gt == 'yes' and r1 == 'safe to share') or (gt == 'no' and r1 == 'needs review')
        correct_r2 = (gt == 'yes' and r2 == 'safe to share') or (gt == 'no' and r2 == 'needs review')

        if correct_r1 and correct_r2 and r1 == r2:
            return 'appropriate_notchange'
        elif not correct_r1 and correct_r2:
            return 'appropriate_change'
        elif correct_r1 and not correct_r2:
            return 'over-reliance'
        elif not correct_r1 and not correct_r2 and r1 == r2:
            return 'under-reliance'
        else:
            return 'other'

    merged['switch_type'] = merged.apply(classify, axis=1)

    total = len(merged)
    pos_notchange = (merged['switch_type'] == 'appropriate_notchange').sum()
    pos_change = (merged['switch_type'] == 'appropriate_change').sum()
    neg = (merged['switch_type'] == 'over-reliance').sum()
    under = (merged['switch_type'] == 'under-reliance').sum()

    return {
        'total_pairs': total,
        'appropriate_notchange': pos_notchange,
        'appropriate_change': pos_change,
        'over_reliance': neg,
        'under_reliance': under,
        'appropriate_notchange_pct': pos_notchange / total if total else 0,
        'appropriate_change_pct': pos_change / total if total else 0,
        'over_pct': neg / total if total else 0,
        'under_pct': under / total if total else 0
    }


csv_dir = 'responses/'
csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

condition_results = []

for file in csv_files:
    df = pd.read_csv(file)
    if 'condition' in df.columns and not df.empty:
        condition = df['condition'].iloc[0]
        breakdown = calculate_switch_breakdown(df)
        breakdown['file'] = os.path.basename(file)
        breakdown['condition'] = condition
        condition_results.append(breakdown)


results_df = pd.DataFrame(condition_results)
summary_df = results_df.groupby('condition').agg({
    'total_pairs': 'sum',
    'appropriate_notchange': 'sum',
    'appropriate_change': 'sum',
    'over_reliance': 'sum',
    'under_reliance': 'sum'
}).reset_index()


summary_df['appropriate_notchange_pct'] = summary_df['appropriate_notchange'] / summary_df['total_pairs']
summary_df['appropriate_change_pct'] = summary_df['appropriate_change'] / summary_df['total_pairs']
summary_df['over_pct'] = summary_df['over_reliance'] / summary_df['total_pairs']
summary_df['under_pct'] = summary_df['under_reliance'] / summary_df['total_pairs']

print("Switch breakdown by condition")
print(summary_df)
