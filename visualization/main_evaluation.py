import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


midpink = (225/255, 149/255, 171/255)
skyblue = (179/255, 218/255, 253/255)
dark_gray = (74/255, 74/255, 74/255)
width = 0.35


# Decision Accuracy data
data1 = {
    'condition': ['Backtranslation', 'Error Highlights', 'LLM Explanation', 'QA Table'],
    'without_mean': [0.602778, 0.592830, 0.634150, 0.659331],
    'without_ci': [0.063121, 0.074852, 0.066631, 0.086177],
    'with_mean': [0.715598, 0.647323, 0.693464, 0.765033],
    'with_ci': [0.065244, 0.082245, 0.062634, 0.082070],
}
df1 = pd.DataFrame(data1)

# CWA data
data2 = {
    'condition': ['Backtranslation', 'Error Highlights', 'LLM Explanation', 'QA Table'],
    'without_mean': [0.188376, 0.156410, 0.231797, 0.282386],
    'without_ci': [0.109289, 0.136049, 0.120657, 0.150915],
    'with_mean': [0.388419, 0.238507, 0.353170, 0.487941],
    'with_ci': [0.116428, 0.149988, 0.111870, 0.155318],
}
df2 = pd.DataFrame(data2)

desired_order = ['Error Highlights', 'LLM Explanation', 'Backtranslation', 'QA Table']

df1 = df1.set_index('condition').loc[desired_order].reset_index()
df2 = df2.set_index('condition').loc[desired_order].reset_index()

x = np.arange(len(df1['condition']))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 3.5), sharey=False)


# ----- Plot 1: Decision Accuracy -----
bars1_1 = ax1.bar(x - width/2, df1['without_mean'], width,
                  color=midpink, label='Independent',
                  yerr=df1['without_ci'], capsize=5, error_kw={'ecolor': dark_gray})
bars1_2 = ax1.bar(x + width/2, df1['with_mean'], width,
                  color=skyblue, label='AI-Assisted', hatch='//',
                  yerr=df1['with_ci'], capsize=5, error_kw={'ecolor': dark_gray})

for bar in bars1_1:
    height = bar.get_height()
    ax1.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width() / 2, height - 0.1),
                 ha='center', va='top', fontsize=10, color='black')

for bar in bars1_2:
    height = bar.get_height()
    ax1.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width() / 2, height - 0.1),
                 ha='center', va='top', fontsize=10, color='black',
                 bbox=dict(boxstyle='round,pad=0.05', facecolor=skyblue, edgecolor='none', alpha=0.9))

ax1.set_title('Decision Accuracy (↑)')
ax1.set_ylabel('Accuracy')
ax1.set_xticks(x)
ax1.set_xticklabels(df1['condition'], fontsize=10)


# ----- Plot 2: CWA -----
bars2_1 = ax2.bar(x - width/2, df2['without_mean'], width,
                  color=midpink, label='Independent',
                  yerr=df2['without_ci'], capsize=5, error_kw={'ecolor': dark_gray})
bars2_2 = ax2.bar(x + width/2, df2['with_mean'], width,
                  color=skyblue, label='AI-Assisted', hatch='//',
                  yerr=df2['with_ci'], capsize=5, error_kw={'ecolor': dark_gray})

for i, bar in enumerate(bars2_1):
    height = bar.get_height()
    if i == 0:
        offset = 0.06
    elif i == 1:
        offset = 0.15
    elif i == 2:
        offset = 0.12
    else:
        offset = 0.18
    ax2.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width() / 2, height - offset),
                 ha='center', va='top', fontsize=10, color='black',
                 bbox=dict(boxstyle='round,pad=0.1', facecolor=midpink, edgecolor='none', alpha=0.9))

for bar in bars2_2:
    height = bar.get_height()
    ax2.annotate(f'{height:.3f}', (bar.get_x() + bar.get_width() / 2, height - 0.17),
                 ha='center', va='top', fontsize=10, color='black',
                 bbox=dict(boxstyle='round,pad=0.05', facecolor=skyblue, edgecolor='none', alpha=0.9))

ax2.set_title('Confidence-Weighted Accuracy (CWA) (↑)')
ax2.set_ylabel('CWA')
ax2.set_xticks(x)
ax2.set_xticklabels(df2['condition'], fontsize=10)


fig.legend(['Independent decision-making', 'AI-Assisted decision-making'],
           loc='lower center', bbox_to_anchor=(0.5, -0.08), ncol=2,
           frameon=True,
           fontsize=11)
fig.subplots_adjust(bottom=0.2, wspace=0.25)

plt.tight_layout()


# Add significance level
def add_significance(ax, x1, x2, y, height, p_label):
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y], lw=1.0, c='black')
    ax.text((x1 + x2) / 2, y + height + 0.01, p_label, ha='center', va='bottom', fontsize=10)


bar_x = dict(zip(df1['condition'], x))
y_base = max(df1[['with_mean', 'without_mean']].max())
step = 0.05

add_significance(ax1,
    x1=bar_x['Backtranslation'] - width/2,
    x2=bar_x['Backtranslation'] + width/2,
    y=y_base + step * 1,
    height=0.015,
    p_label='***')

add_significance(ax1,
    x1=bar_x['LLM Explanation'] - width/2,
    x2=bar_x['LLM Explanation'] + width/2,
    y=y_base + step * 1,
    height=0.015,
    p_label='*')

add_significance(ax1,
    x1=bar_x['QA Table'] - width/2,
    x2=bar_x['QA Table'] + width/2,
    y=y_base + step * 2,
    height=0.015,
    p_label='***')

add_significance(ax1,
    x1=bar_x['LLM Explanation'] + width/2,
    x2=bar_x['QA Table'] + width/2,
    y=y_base + step * 4,
    height=0.015,
    p_label='*')

add_significance(ax1,
    x1=bar_x['Error Highlights'] + width/2,
    x2=bar_x['QA Table'] + width/2,
    y=y_base + step * 6,
    height=0.015,
    p_label='***')

ax1.set_ylim(0, y_base + step * 8)


bar_x2 = dict(zip(df2['condition'], x))
y_base2 = max(df2[['with_mean', 'without_mean']].max())
step2 = 0.05  # vertical step

add_significance(ax2,
    x1=bar_x2['Backtranslation'] - width/2,
    x2=bar_x2['Backtranslation'] + width/2,
    y=y_base2 + step2 * 1,
    height=0.015,
    p_label='***')

add_significance(ax2,
    x1=bar_x2['Error Highlights'] - width/2,
    x2=bar_x2['Error Highlights'] + width/2,
    y=y_base2 + step2 * 1,
    height=0.015,
    p_label='*')

add_significance(ax2,
    x1=bar_x2['LLM Explanation'] - width/2,
    x2=bar_x2['LLM Explanation'] + width/2,
    y=y_base2 + step2 * 1,
    height=0.015,
    p_label='**')

add_significance(ax2,
    x1=bar_x2['QA Table'] - width/2,
    x2=bar_x2['QA Table'] + width/2,
    y=y_base2 + step2 * 3.5,
    height=0.015,
    p_label='***')

add_significance(ax2,
    x1=bar_x2['Error Highlights'] + width/2,
    x2=bar_x2['Backtranslation'] + width/2,
    y=y_base2 + step2 * 3,
    height=0.015,
    p_label='*')

add_significance(ax2,
    x1=bar_x2['LLM Explanation'] + width/2,
    x2=bar_x2['Error Highlights'] + width/2,
    y=y_base2 + step2 * 5,
    height=0.015,
    p_label='*')

add_significance(ax2,
    x1=bar_x2['LLM Explanation'] + width/2,
    x2=bar_x2['QA Table'] + width/2,
    y=y_base2 + step2 * 6,
    height=0.015,
    p_label='*')

add_significance(ax2,
    x1=bar_x2['Error Highlights'] + width/2,
    x2=bar_x2['QA Table'] + width/2,
    y=y_base2 + step2 * 8,
    height=0.015,
    p_label='***')

add_significance(ax2,
    x1=bar_x2['Error Highlights'] - width/2,
    x2=bar_x2['QA Table'] - width/2,
    y=y_base2 + step2 * 10,
    height=0.015,
    p_label='*')

ax2.set_ylim(0, y_base2 + step2 * 12)

plt.savefig('main_evaluation.png', dpi=300, bbox_inches='tight')
plt.show()
