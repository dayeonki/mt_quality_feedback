import pandas as pd

df = pd.read_csv('total_summary.csv')
high_accuracy = df[df['accuracy_total'] > 0.7]

print("Annotators with accuracy_total > 0.7:")
print(high_accuracy['annotator_id'].tolist())