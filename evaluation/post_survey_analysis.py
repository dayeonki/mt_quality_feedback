import pandas as pd


df = pd.read_csv('results.csv')

df['time_taken'] = pd.to_timedelta(df['time_taken'])

# --- 1. Means per Condition Group ---
means_by_condition = df.groupby('condition').agg({
    'workload': 'mean',
    'helpfulness': 'mean',
    'trust': 'mean',
    'en_proficiency': 'mean',
    'target_proficiency': 'mean',
    'mt_frequency': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],  # If categorical
    'time_taken': 'mean'
}).reset_index()

means_by_condition['time_taken'] = means_by_condition['time_taken'].astype(str)

# --- 2. Overall Means (Total) ---
overall_means = {
    'en_proficiency_mean': df['en_proficiency'].mean(),
    'target_proficiency_mean': df['target_proficiency'].mean(),
    'mt_frequency_mode': df['mt_frequency'].mode()[0] if not df['mt_frequency'].mode().empty else df['mt_frequency'].iloc[0],
    'time_taken_mean': str(df['time_taken'].mean())
}

# --- 3. Counts of first_language ---
df['first_language'] = df['first_language'].str.strip().str.lower()
language_counts = df['first_language'].value_counts()

mt_frequency_counts = df['mt_frequency'].value_counts()
print("\nCounts of mt_frequency:")
print(mt_frequency_counts)

print("Means by condition group:")
print(means_by_condition)

print("\nOverall Means:")
print(overall_means)

print("\nCounts of first_language:")
print(language_counts)
