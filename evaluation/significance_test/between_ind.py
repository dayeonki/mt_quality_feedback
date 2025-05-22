import pandas as pd
from scipy.stats import ttest_ind
from itertools import combinations

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


df = pd.read_csv('../results.csv')

DV_COL = 'DV_ShareabilityAccuracy'
conditions = ['annotation', 'bt', 'askqe', 'explanation']
baseline_sets = {}

for cond in conditions:
    cond_df = df[df['IV_Condition'] == cond][['ID_ParticipantID', 'ID_StimulusID']]
    
    merged = pd.merge(
        cond_df,
        df[df['IV_Condition'] == 'baseline'],
        on=['ID_ParticipantID', 'ID_StimulusID'],
        how='inner'
    )
    
    baseline_sets[cond] = merged[DV_COL].dropna()


def pval_to_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return ''


results = {}

for cond1, cond2 in combinations(conditions, 2):
    vals1 = baseline_sets[cond1]
    vals2 = baseline_sets[cond2]
    t_stat, p_val = ttest_ind(vals1, vals2, equal_var=False)
    results[f'{cond1} baseline vs {cond2} baseline'] = {
        'n1': len(vals1),
        'n2': len(vals2),
        't_stat': t_stat,
        'p_value': p_val,
        f'mean_{cond1}': vals1.mean(),
        f'sem_{cond1}': vals1.std(ddof=1) / (len(vals1) ** 0.5),
        f'mean_{cond2}': vals2.mean(),
        f'sem_{cond2}': vals2.std(ddof=1) / (len(vals2) ** 0.5)
    }


for pair, res in results.items():
    stars = pval_to_stars(res['p_value'])

    cond1_key = [k for k in res.keys() if k.startswith('mean_')][0].replace('mean_', '')
    cond2_key = [k for k in res.keys() if k.startswith('mean_')][1].replace('mean_', '')

    print(f'{pair}: t={res["t_stat"]:.3f}, p={res["p_value"]:.4f} {stars}')
    print(f'  → {cond1_key} baseline: {res[f"mean_{cond1_key}"]:.3f} ± {res[f"sem_{cond1_key}"]:.3f}')
    print(f'     {cond2_key} baseline: {res[f"mean_{cond2_key}"]:.3f} ± {res[f"sem_{cond2_key}"]:.3f}')
