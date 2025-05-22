import pandas as pd
from scipy.stats import ttest_rel


df = pd.read_csv('summary.csv')

DV_COL = 'DV_ShareabilityAccuracy'
comparison_conditions = ['annotation', 'bt', 'askqe', 'explanation']
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


for cond in comparison_conditions:
    baseline_df = df[df['IV_Condition'] == 'baseline']
    comp_df = df[df['IV_Condition'] == cond]
    
    merged = pd.merge(
        baseline_df,
        comp_df,
        on=['ID_ParticipantID', 'ID_StimulusID'],
        suffixes=('_baseline', f'_{cond}')
    )
    
    if len(merged) < 2:
        print(f'Not enough pairs for baseline vs. {cond}')
        continue

    t_stat, p_val = ttest_rel(
        merged[f'{DV_COL}_baseline'],
        merged[f'{DV_COL}_{cond}']
    )

    mean_baseline = merged[f'{DV_COL}_baseline'].mean()
    mean_cond = merged[f'{DV_COL}_{cond}'].mean()

    sem_baseline = merged[f'{DV_COL}_baseline'].std(ddof=1) / (len(merged) ** 0.5)
    sem_cond = merged[f'{DV_COL}_{cond}'].std(ddof=1) / (len(merged) ** 0.5)

    results[cond] = {
        'n_pairs': len(merged),
        't_stat': t_stat,
        'p_value': p_val,
        'mean_baseline': mean_baseline,
        'sem_baseline': sem_baseline,
        'mean_' + cond: mean_cond,
        'sem_' + cond: sem_cond
    }

for cond, res in results.items():
    stars = pval_to_stars(res['p_value'])
    print(f'Baseline vs. {cond}: t={res["t_stat"]:.3f}, p={res["p_value"]:.4f} {stars}')
    print(f'  → Mean baseline: {res["mean_baseline"]:.3f} ± {res["sem_baseline"]:.3f}')
    print(f'     Mean {cond}: {res["mean_" + cond]:.3f} ± {res["sem_" + cond]:.3f}')
