import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data = {
    'condition': ['Error Highlights', 'QA Table', 'Backtranslation', 'LLM Explanation'],
    'appropriate_notchange_pct': [0.502793, 0.580282, 0.527778, 0.498599],
    'appropriate_change_pct': [0.145251, 0.185915, 0.188889, 0.193277],
    'over_pct': [0.094972, 0.078873, 0.072222, 0.134454],
    'under_pct': [0.256983, 0.154930, 0.211111, 0.173669],
    'appropriate_notchange_n': [180, 211, 190, 178],
    'appropriate_change_n': [52, 66, 68, 69],
    'over_n': [36, 28, 26, 48],
    'under_n': [92, 55, 76, 65],
}

df = pd.DataFrame(data)

desired_order = ['Error Highlights', 'LLM Explanation', 'Backtranslation', 'QA Table']
df['condition'] = pd.Categorical(df['condition'], categories=desired_order, ordered=True)
df = df.sort_values('condition').reset_index(drop=True)


x = np.arange(len(df))
width = 0.6

color_good_nochange = (200/255, 230/255, 201/255)  # light green
color_good_change = (129/255, 199/255, 132/255)    # medium green
color_over = (239/255, 83/255, 80/255)             # light red
color_under = (255/255, 183/255, 178/255)          # darker red

fig, ax = plt.subplots(figsize=(5, 2.5))


p1 = ax.bar(x, df['appropriate_notchange_pct'], width, color=color_good_nochange, label='Appropriate (No Switch)')
p2 = ax.bar(x, df['appropriate_change_pct'], width, bottom=df['appropriate_notchange_pct'],
            color=color_good_change, label='Appropriate (Switch)')
p3 = ax.bar(x, df['over_pct'], width,
            bottom=df['appropriate_notchange_pct'] + df['appropriate_change_pct'],
            color=color_over, label='Over-reliance')
p4 = ax.bar(x, df['under_pct'], width,
            bottom=df['appropriate_notchange_pct'] + df['appropriate_change_pct'] + df['over_pct'],
            color=color_under, label='Under-reliance')


for i in range(len(df)):
    y0 = df.loc[i, 'appropriate_notchange_pct'] / 2
    y1 = df.loc[i, 'appropriate_notchange_pct'] + df.loc[i, 'appropriate_change_pct'] / 2
    y2 = df.loc[i, 'appropriate_notchange_pct'] + df.loc[i, 'appropriate_change_pct'] + df.loc[i, 'over_pct'] / 2
    y3 = df.loc[i, 'appropriate_notchange_pct'] + df.loc[i, 'appropriate_change_pct'] + df.loc[i, 'over_pct'] + df.loc[i, 'under_pct'] / 2

    ax.annotate(f'n={df["appropriate_notchange_n"][i]}', (x[i], y0), ha='center', va='center', fontsize=8)
    ax.annotate(f'n={df["appropriate_change_n"][i]}', (x[i], y1), ha='center', va='center', fontsize=8)
    ax.annotate(f'n={df["over_n"][i]}', (x[i], y2), ha='center', va='center', fontsize=8)
    ax.annotate(f'n={df["under_n"][i]}', (x[i], y3), ha='center', va='center', fontsize=8)


ax.set_ylabel('Proportion of Examples', fontsize=10)
ax.set_title('Switch Percentage Breakdown', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(df['condition'], fontsize=8)
ax.set_ylim(0, 1)
fig.legend(
    loc='upper center',
    bbox_to_anchor=(0.53, 0.05),
    ncol=2,
    fontsize=9,
)
plt.tight_layout()
plt.savefig('switch_percentage.png', dpi=300, bbox_inches='tight')
plt.show()
