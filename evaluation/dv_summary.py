import pandas as pd
import scipy.stats as stats
import numpy as np
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('results.csv')

def describe_with_ci(group, column):
    desc = group[column].describe()
    count = desc['count']
    mean = desc['mean']
    std = desc['std']
    sem = std / np.sqrt(count)
    ci = 1.96 * sem  # 95% confidence interval using normal approximation
    return pd.Series({
        'count': count,
        'mean': round(mean, 6),
        'std': round(std, 6),
        'min': desc['min'],
        '25%': desc['25%'],
        '50%': desc['50%'],
        '75%': desc['75%'],
        'max': desc['max'],
        '95% CI Lower': round(mean - ci, 6),
        '95% CI Upper': round(mean + ci, 6)
    })

for metric in ['accuracy_total', 'accuracy_without', 'accuracy_with', 'cwa_total', 'cwa_without', 'cwa_with', 'confidence_total', 'confidence_without', 'confidence_with']:
    print(f"\n{metric.replace('_', ' ').title()}")
    summary = df.groupby('condition').apply(lambda g: describe_with_ci(g, metric))
    print(summary)
