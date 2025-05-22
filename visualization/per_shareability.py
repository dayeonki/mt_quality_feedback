import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Decision Accuracy data
data1 = {
    'condition': ['Independent', 'Independent',
                  'Backtranslation', 'Backtranslation',
                  'Error Highlights', 'Error Highlights',
                  'LLM Explanation', 'LLM Explanation',
                  'QA Table', 'QA Table'],
    'shareable': ['No', 'Yes'] * 5,
    'mean': [0.509722, 0.733057,
             0.622093, 0.804598,
             0.546448, 0.752747,
             0.680851, 0.708995,
             0.687151, 0.848315],
    'ci_lower': [0.473181, 0.700789,
                 0.549419, 0.745511,
                 0.474120, 0.689896,
                 0.614039, 0.644064,
                 0.619036, 0.795468],
    'ci_upper': [0.546263, 0.765324,
                 0.694767, 0.863684,
                 0.618776, 0.815598,
                 0.747664, 0.773925,
                 0.755265, 0.901162],
}

# CWA data
data2 = {
    'condition': ['Independent', 'Independent',
                  'Backtranslation', 'Backtranslation',
                  'Error Highlights', 'Error Highlights',
                  'LLM Explanation', 'LLM Explanation',
                  'QA Table', 'QA Table'],
    'shareable': ['No', 'Yes'] * 5,
    'mean': [0.023889, 0.401936,
             0.210465, 0.565517,
             0.068852, 0.415385,
             0.323404, 0.379894,
             0.336313, 0.649438],
    'ci_lower': [-0.033625, 0.351141,
                 0.081843, 0.466857,
                 -0.051151, 0.310309,
                 0.204173, 0.266084,
                 0.217301, 0.553653],
    'ci_upper': [0.081402, 0.452732,
                 0.339087, 0.664178,
                 0.188856, 0.520461,
                 0.442635, 0.493704,
                 0.455325, 0.745223],
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

desired_order = ['Independent', 'Error Highlights', 'LLM Explanation', 'Backtranslation', 'QA Table']


df1['condition'] = pd.Categorical(df1['condition'], categories=desired_order, ordered=True)
df1 = df1.sort_values('condition').reset_index(drop=True)

df2['condition'] = pd.Categorical(df2['condition'], categories=desired_order, ordered=True)
df2 = df2.sort_values('condition').reset_index(drop=True)


df1['ci'] = df1['ci_upper'] - df1['mean']
df2['ci'] = df2['ci_upper'] - df2['mean']

conditions = df1['condition'].unique()
x = np.arange(len(conditions))
width = 0.38
dark_gray = (74/255, 74/255, 74/255)
green_alpha = (134/255, 204/255, 120/255)
red_alpha = (204/255, 55/255, 55/255, 0.7)

# Split by shareable label
df1_no = df1[df1['shareable'] == 'No'].reset_index(drop=True)
df1_yes = df1[df1['shareable'] == 'Yes'].reset_index(drop=True)
df2_no = df2[df2['shareable'] == 'No'].reset_index(drop=True)
df2_yes = df2[df2['shareable'] == 'Yes'].reset_index(drop=True)



fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,3), sharey=False)

# Plot 1: Decision Accuracy
bars1_no = ax1.bar(x - width/2, df1_no['mean'], width,
                   label='Needs bilingual review before sharing',
                   color=red_alpha, yerr=df1_no['ci'], capsize=5,
                   error_kw={'ecolor': dark_gray})

bars1_yes = ax1.bar(x + width/2, df1_yes['mean'], width,
                    label='Safe to share as-is',
                    color=green_alpha, hatch='//', yerr=df1_yes['ci'], capsize=5,
                    error_kw={'ecolor': dark_gray})

for bar in bars1_no:
    height = bar.get_height()
    ax1.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width()/2, height - 0.17),
                 textcoords="offset points", xytext=(0, 3),
                 ha='center', va='bottom', fontsize=9)

for bar in bars1_yes:
    height = bar.get_height()
    ax1.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width()/2, height - 0.17),
                 textcoords="offset points", xytext=(0, 3),
                 ha='center', va='bottom', fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.1', facecolor=green_alpha, edgecolor='none'))

ax1.set_ylabel('Accuracy')
ax1.set_title('Decision Accuracy (↑)')
ax1.set_xticks(x)
ax1.set_xticklabels(conditions, fontsize=10)
ax1.set_ylim(0, 1.05)


# Plot 2: CWA
bars2_no = ax2.bar(x - width/2, df2_no['mean'], width,
                   color=red_alpha, yerr=df2_no['ci'], capsize=5,
                   error_kw={'ecolor': dark_gray})

bars2_yes = ax2.bar(x + width/2, df2_yes['mean'], width,
                    color=green_alpha, hatch='//', yerr=df2_yes['ci'], capsize=5,
                    error_kw={'ecolor': dark_gray})

for i, bar in enumerate(bars2_no):
    height = bar.get_height()
    offset = 0.18 if i == 0 else 0.24
    ax2.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width()/2, height - offset),
                 textcoords="offset points", xytext=(0, 3),
                 ha='center', va='bottom', fontsize=9)

for bar in bars2_yes:
    height = bar.get_height()
    ax2.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width()/2, height - 0.22),
                 textcoords="offset points", xytext=(0, 3),
                 ha='center', va='bottom', fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.1', facecolor=green_alpha, edgecolor='none'))


ax1.annotate('n=\n720',
             xy=(bars1_no[0].get_x() + bars1_no[0].get_width()/2, 0.03),
             ha='center', va='bottom', fontsize=9, color='white')


ax1.annotate('n=\n180',
             xy=(bars1_no[1].get_x() + bars1_no[1].get_width()/2, 0.03),
             ha='center', va='bottom', fontsize=9, color='white')

ax1.annotate('n=\n180',
             xy=(bars1_no[2].get_x() + bars1_no[2].get_width()/2, 0.03),
             ha='center', va='bottom', fontsize=9, color='white')

ax1.annotate('n=\n180',
             xy=(bars1_no[3].get_x() + bars1_no[3].get_width()/2, 0.03),
             ha='center', va='bottom', fontsize=9, color='white')

ax1.annotate('n=\n180',
             xy=(bars1_no[4].get_x() + bars1_no[4].get_width()/2, 0.03),
             ha='center', va='bottom', fontsize=9, color='white')


ax2.set_ylabel('CWA')
ax2.set_title('Confidence-Weighted Accuracy (CWA) (↑)')
ax2.set_xticks(x)
ax2.set_xticklabels(conditions, fontsize=10)
ax2.set_ylim(-0.25, 1.05)

fig.legend(['Needs bilingual review before sharing', 'Safe to share as-is'],
           loc='lower center', bbox_to_anchor=(0.5, -0.08), ncol=2,
           frameon=True, fontsize=10)

fig.subplots_adjust(bottom=0.25, wspace=0.3)
plt.tight_layout()


# Add significance levels
def add_significance(ax, x1, x2, y, height, p_label):
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y],
            lw=1.0, c='black')
    ax.text((x1 + x2)/2, y + height + 0.01, p_label,
            ha='center', va='bottom', fontsize=10)


y_base1 = max(df1['mean'])
step1 = 0.05
bar_x1 = dict(zip(conditions, x))


add_significance(ax1,
    bar_x1['Independent'] - width/2,
    bar_x1['Independent'] + width/2,
    y_base1 + step1 * 2, height=0.015, p_label='***')

add_significance(ax1,
    bar_x1['Backtranslation'] - width/2,
    bar_x1['Backtranslation'] + width/2,
    y_base1 + step1 * 2, height=0.015, p_label='***')

add_significance(ax1,
    bar_x1['QA Table'] - width/2,
    bar_x1['QA Table'] + width/2,
    y_base1 + step1 * 2, height=0.015, p_label='***')
    
add_significance(ax1,
    bar_x1['Error Highlights'] - width/2,
    bar_x1['Error Highlights'] + width/2,
    y_base1 + step1 * 2, height=0.015, p_label='**')

ax1.set_ylim(0, y_base1 + step1 * 5)


y_base2 = max(df2['mean'])
step2 = 0.08
bar_x2 = dict(zip(conditions, x))


for cond in conditions:
    if cond != 'LLM Explanation':
        add_significance(ax2,
            bar_x2[cond] - width/2,
            bar_x2[cond] + width/2,
            y_base2 + step2 * 2, height=0.015,
            p_label='***')

ax2.set_ylim(-0.25, y_base2 + step2 * 5)


plt.savefig('per_shareability.png', dpi=300, bbox_inches='tight')
plt.show()
