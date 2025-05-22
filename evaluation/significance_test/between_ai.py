import pandas as pd
from scipy.stats import ttest_ind
from itertools import combinations

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


df = pd.read_csv('r_analysis2.csv')

DV_COL = 'DV_CWA'
conditions = ['annotation', 'bt', 'askqe', 'explanation']
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


# Compare each pair of conditions
for cond1, cond2 in combinations(conditions, 2):
    vals1 = df[df['IV_Condition'] == cond1][DV_COL].dropna()
    vals2 = df[df['IV_Condition'] == cond2][DV_COL].dropna()
    t_stat, p_val = ttest_ind(vals1, vals2, equal_var=False)  # Welch's t-test

    results[f'{cond1} vs {cond2}'] = {
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
    print(f'{pair}: t={res["t_stat"]:.3f}, p={res["p_value"]:.4f} {stars}')
    cond1, cond2 = pair.split(' vs ')
    print(f'  → {cond1}: {res[f"mean_{cond1}"]:.3f} ± {res[f"sem_{cond1}"]:.3f}')
    print(f'     {cond2}: {res[f"mean_{cond2}"]:.3f} ± {res[f"sem_{cond2}"]:.3f}')
