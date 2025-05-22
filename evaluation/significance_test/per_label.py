import pandas as pd
from scipy.stats import ttest_ind


df = pd.read_csv('results.csv')

df['IV_Shareable'] = df['IV_Shareable'].astype(str).str.lower()
DV_COL = 'DV_CWA'
conditions = ['baseline', 'askqe', 'bt', 'explanation', 'annotation']
results = {}


def pval_to_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return ''


for cond in conditions:
    cond_df = df[df['IV_Condition'] == cond]
    
    yes_vals = cond_df[cond_df['IV_Shareable'] == 'yes'][DV_COL].dropna()
    no_vals = cond_df[cond_df['IV_Shareable'] == 'no'][DV_COL].dropna()

    if len(yes_vals) < 2 or len(no_vals) < 2:
        print(f'Not enough data for {cond} (yes={len(yes_vals)}, no={len(no_vals)})')
        continue

    # Welch's t-test
    t_stat, p_val = ttest_ind(yes_vals, no_vals, equal_var=False)

    results[cond] = {
        'n_yes': len(yes_vals),
        'n_no': len(no_vals),
        't_stat': t_stat,
        'p_value': p_val,
        'mean_yes': yes_vals.mean(),
        'sem_yes': yes_vals.std(ddof=1) / (len(yes_vals) ** 0.5),
        'mean_no': no_vals.mean(),
        'sem_no': no_vals.std(ddof=1) / (len(no_vals) ** 0.5)
    }

for cond, res in results.items():
    stars = pval_to_stars(res['p_value'])
    print(f'{cond}: t={res["t_stat"]:.3f}, p={res["p_value"]:.4f} {stars}')
    print(f'  → Yes: {res["mean_yes"]:.3f} ± {res["sem_yes"]:.3f} (n={res["n_yes"]})')
    print(f'     No: {res["mean_no"]:.3f} ± {res["sem_no"]:.3f} (n={res["n_no"]})')
