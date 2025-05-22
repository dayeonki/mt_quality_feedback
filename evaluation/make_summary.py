import pandas as pd
import warnings
import os
import glob


warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)


def map_shareability_to_tf(shareability):
    if shareability == 'good':
        return 'no_error'
    elif shareability == 'minor':
        return 'minor'
    elif shareability == 'bad':
        return 'critical'
    return None


def evaluate_file(input_file):
    df = pd.read_csv(input_file)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    postsurvey_row = df[df['id'] == 'POSTSURVEY'].iloc[0]

    # Pre-survey Q
    first_language = df.iloc[0]['first_language']
    en_proficiency = df.iloc[0]['en_proficiency']
    target_proficiency = df.iloc[0]['target_proficiency']
    mt_frequency = df.iloc[0]['mt_frequency']
    condition = df.iloc[0]['condition']

    # Post-survey Q
    helpfulness = postsurvey_row['helpfulness']
    trust = postsurvey_row['trust']
    workload = postsurvey_row['workload']

    time_diff = df['timestamp'].max() - df['timestamp'].min()
    formatted_time = str(time_diff).split()[-1]


    def attention_check_auto(df):
        results = []
        # Get all IDs that end with '_attn'
        attn_ids = df[df['id'].str.endswith('_attn')]['id'].unique()

        # Extract base IDs by removing '_attn'
        base_ids = [attn_id.replace('_attn', '') for attn_id in attn_ids]

        for base_id in base_ids:
            row_main = df[df['id'] == base_id]
            row_attn = df[df['id'] == f'{base_id}_attn']
            if not row_main.empty and not row_attn.empty:
                shareability_match = row_main['shareability_response'].values[0] == row_attn['shareability_response'].values[0]
                passed = bool(shareability_match)
            else:
                passed = False
            results.append({
                'id': base_id,
                'attention_check_passed': passed
            })
        return results


    def average_confidence_scores(df):
        # Exclude post-survey and attention check rows
        data_df = df[~df['id'].astype(str).str.contains('POSTSURVEY|attn', na=False)].copy()

        data_df['confidence_response'] = pd.to_numeric(data_df['confidence_response'], errors='coerce')
        valid_df = data_df.dropna(subset=['confidence_response'])
        total_conf = valid_df['confidence_response'].mean()

        conf_is_error_no = valid_df[valid_df['is_shareable'] == 'no']['confidence_response'].mean()
        conf_is_error_yes = valid_df[valid_df['is_shareable'] == 'yes']['confidence_response'].mean()

        conf_step_1 = valid_df[valid_df['step'] == 1]['confidence_response'].mean()
        conf_step_2 = valid_df[valid_df['step'] == 2]['confidence_response'].mean()

        return {
            'total': total_conf,
            'is_shareable_no': conf_is_error_no,
            'is_shareable_yes': conf_is_error_yes,
            'confidence_without': conf_step_1,
            'confidence_with': conf_step_2
        }

    def accuracy_shareability():
        # Exclude post-survey and attention check rows
        data_df = df[~df['id'].astype(str).str.contains('POSTSURVEY|attn', na=False)].copy()
        
        def get_correct_shareability(row):
            if row['is_shareable'] == 'no':
                return 'needs review'
            elif row['is_shareable'] == 'yes':
                return 'safe to share'
            return None

        data_df['correct_shareability'] = data_df.apply(get_correct_shareability, axis=1)
        data_df['is_shareability_correct'] = data_df['shareability_response'] == data_df['correct_shareability']

        total_acc = data_df['is_shareability_correct'].mean()
        acc_is_error_no = data_df[data_df['is_shareable'] == 'no']['is_shareability_correct'].mean()
        acc_is_error_yes = data_df[data_df['is_shareable'] == 'yes']['is_shareability_correct'].mean()

        acc_step_1 = data_df[data_df['step'] == 1]['is_shareability_correct'].mean()
        acc_step_2 = data_df[data_df['step'] == 2]['is_shareability_correct'].mean()

        updated_df = data_df

        return {
            'total': total_acc,
            'is_shareable_no': acc_is_error_no,
            'is_shareable_yes': acc_is_error_yes,
            'accuracy_without': acc_step_1,
            'accuracy_with': acc_step_2
        }, updated_df


    def confidence_weighted_accuracy(df):
        data_df = df[~df['id'].astype(str).str.contains('POSTSURVEY|attn', na=False)].copy()

        if 'is_shareability_correct' not in data_df.columns:
            raise ValueError("Missing column 'is_shareability_correct'. Run accuracy_shareability first.")
        
        valid_df = data_df.dropna(subset=['is_shareability_correct', 'confidence_response']).copy()
        valid_df['confidence_response'] = pd.to_numeric(valid_df['confidence_response'], errors='coerce')
        valid_df['sign'] = valid_df['is_shareability_correct'].apply(lambda x: 1 if x else -1)
        valid_df['weighted_score'] = valid_df['sign'] * (valid_df['confidence_response'] / 5)

        total_cwa = valid_df['weighted_score'].mean()
        baseline_cwa = valid_df[valid_df['is_shareable'] == 'no']['weighted_score'].mean()
        condition_cwa = valid_df[valid_df['is_shareable'] == 'yes']['weighted_score'].mean()

        cwa_step_1 = valid_df[valid_df['step'] == 1]['weighted_score'].mean()
        cwa_step_2 = valid_df[valid_df['step'] == 2]['weighted_score'].mean()

        return {
            'total': total_cwa,
            'is_shareable_no': baseline_cwa,
            'is_shareable_yes': condition_cwa,
            'cwa_without': cwa_step_1,
            'cwa_with': cwa_step_2
        }
    

    attention_pass = attention_check_auto(df)
    accuracy, updated_df = accuracy_shareability()
    cwa = confidence_weighted_accuracy(updated_df)
    confidence = average_confidence_scores(df)

    return {
        'annotator_id': os.path.basename(input_file).replace('.csv', ''),
        'condition': condition,
        'first_language': first_language,
        'en_proficiency': en_proficiency,
        'target_proficiency': target_proficiency,
        'mt_frequency': mt_frequency,
        'workload': workload,
        'helpfulness': helpfulness,
        'trust': trust,
        'time_taken': formatted_time,
        'attention_pass': attention_pass,
        'accuracy_total': accuracy['total'],
        'accuracy_no': accuracy['is_shareable_no'],
        'accuracy_yes': accuracy['is_shareable_yes'],
        'accuracy_without': accuracy['accuracy_without'],
        'accuracy_with': accuracy['accuracy_with'],
        'cwa_total': cwa['total'],
        'cwa_no': cwa['is_shareable_no'],
        'cwa_yes': cwa['is_shareable_yes'],
        'cwa_without': cwa['cwa_without'],
        'cwa_with': cwa['cwa_with'],
        'confidence_total': confidence['total'],
        'confidence_no': confidence['is_shareable_no'],
        'confidence_yes': confidence['is_shareable_yes'],
        'confidence_without': confidence['confidence_without'],
        'confidence_with': confidence['confidence_with'],
    }


if __name__ == "__main__":
    results = []
    for file in glob.glob('responses/*.csv'):
        try:
            result = evaluate_file(file)
            results.append(result)
        except Exception as e:
            print(f"Error in {file}: {e}")

    pd.DataFrame(results).to_csv('results.csv', index=False)
