import pandas as pd
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa


df = pd.read_csv('annotation.csv', sep=',')

annotator_cols = ['annotator_1', 'annotator_2', 'annotator_3', 'annotator_4', 'annotator_5']
all_labels = sorted(set(val for row in df[annotator_cols].values for val in row))

def get_label_counts(row, labels):
    counts = [list(row).count(label) for label in labels]
    return counts

label_count_matrix = df[annotator_cols].apply(lambda row: get_label_counts(row, all_labels), axis=1)
label_count_matrix = np.array(label_count_matrix.tolist())


# Fleiss' Kappa
kappa = fleiss_kappa(label_count_matrix)
print(f"Fleiss' Kappa (overall): {kappa:.4f}")


# Majority vote
def majority_agreement(counts):
    return max(counts) / sum(counts)

df['percent_agreement'] = [majority_agreement(counts) for counts in label_count_matrix]

def agreement_score(counts):
    n = sum(counts)
    if n <= 1:
        return 1.0  # If only one rater, trivially perfect agreement
    p_bar = sum(c * (c - 1) for c in counts) / (n * (n - 1))
    return p_bar


df['agreement_score'] = [agreement_score(counts) for counts in label_count_matrix]
df.to_csv('agreement.csv', index=False)
