from flask import Flask, request
from flask import render_template
import time
import ast
import os
import csv
import pandas as pd
import json
import random


# ---------------------------------Configuration---------------------------------
config = {
    1: {'askqe': True},
    2: {'bt': True},
    3: {'annotation': True},
    4: {'explanation': True},
}

tracker_dir = 'tracker'

samples_tracked = {
    1: json.load(open(f'{tracker_dir}/askqe.json', 'r')),
    2: json.load(open(f'{tracker_dir}/bt.json', 'r')),
    3: json.load(open(f'{tracker_dir}/annotation.json', 'r')),
    4: json.load(open(f'{tracker_dir}/explanation.json', 'r')),
}

num_samples= 20
num_responses = 1


# ---------------------------------Sample & ID---------------------------------
def sample(examples, num_samples):
    examples = {key:value for key, value in examples.items() if value>-1}
    values = [value for key, value in examples.items() if value<num_responses]
    if values:
        candidates = [key for key,value in examples.items() if value==min(values)]
    else:
        return None
    if len(candidates) < num_samples:
        return None
    samples = random.sample(candidates, num_samples)
    samples = [int(e) for e in samples]
    return samples


def condition_to_idx(data):
    condition_str = data.get('condition', '')
    condition_mapping = {
        'askqe': 1,
        'bt': 2,
        'annotation': 3,
        'explanation': 4,
    }
    if condition_str in condition_mapping:
        return condition_mapping[condition_str]  # Convert string to corresponding index
    else:
        raise ValueError(f"Invalid condition: {condition_str}. Must be one of {list(condition_mapping.keys())}.")


def idx_to_condition(idx):
    if config[idx].get('askqe', False):
        return 'askqe'
    elif config[idx].get('bt', False):
        return 'bt'
    elif config[idx].get('annotation', False):
        return 'annotation'
    elif config[idx].get('explanation', False):
        return 'explanation'
    return 'false'


# ---------------------------------Save Responses---------------------------------
def save_response(data):
    save_name = time.strftime("%Y%m%d-%H%M%S")
    response_file = f'responses/{save_name}.json'
    with open(response_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    sample_ids = [int(e) for e in data['sample_indices'].split(",")]  # IDs instead of index
    condition_idx = condition_to_idx(data)  # Get numerical condition index
    condition_str = idx_to_condition(condition_idx)  # Convert index to 'askqe', 'bt', or 'annotation'

    for example_id in sample_ids:
        if example_id in samples_tracked[condition_idx]:  # Check if ID exists
            samples_tracked[condition_idx][example_id] = abs(samples_tracked[condition_idx][example_id])
        else:
            print(f'Error: ID {example_id} not found in tracker!')

    tracker_filename = f'{tracker_dir}/{condition_str}.json'
    with open(tracker_filename, 'w') as f:
        json.dump(samples_tracked[condition_idx], f, ensure_ascii=False, indent=4)

    return 'Your response will be manually approved shortly.'


# ---------------------------------Get Examples---------------------------------
def hold_examples(tracker, examples):
    for ins in examples:
        if tracker[f'{ins}'] == 0:
            tracker[f'{ins}'] = -1
        else:
            tracker[f'{ins}'] = -abs(tracker[f'{ins}'] + 1)


def parse_list(value):
    if isinstance(value, str):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return []
    return value


def get_next_condition_round_robin():
    last_idx_path = os.path.join(tracker_dir, 'last_condition.txt')

    # Read last used condition index
    if os.path.exists(last_idx_path):
        with open(last_idx_path, 'r') as f:
            last = int(f.read().strip())
    else:
        last = 0  # Start from beginning if file is missing

    # Try next 4 possible conditions in round-robin
    for offset in range(1, 5):
        next_idx = (last + offset - 1) % 4 + 1
        tracker = samples_tracked[next_idx]
        unfinished = [i for i in tracker if tracker[i] < num_responses]

        if unfinished:
            # Update the last used condition
            with open(last_idx_path, 'w') as f:
                f.write(str(next_idx))
            return next_idx

    return None


def get_examples():    
    condition = get_next_condition_round_robin()
    if condition is None:
        return None, None

    df = pd.read_csv("examples/enes_examples.csv")
    df["id"] = df["id"].astype(int)  # Ensure ID column is integer

    all_ids = df["id"].tolist()
    random.shuffle(all_ids)

    sampled_ids = [eid for eid in all_ids if str(eid) in samples_tracked[condition]]

    if len(sampled_ids) < num_samples:
        return None, None

    sampled_ids = sampled_ids[:num_samples]
    hold_examples(samples_tracked[condition], sampled_ids)

    condition_name = idx_to_condition(condition)

    with open(f'{tracker_dir}/{condition_name}.json', 'w') as f:
        json.dump(samples_tracked[condition], f, ensure_ascii=False, indent=4)

    df_filtered = df[df["id"].isin(sampled_ids)].set_index("id").loc[sampled_ids].reset_index()

    selected_examples = []
    for _, row in df_filtered.iterrows():
        selected_fields = {
            "id": row["id"],
            "is_shareable": row.get("is_shareable", ""),
            "pert_type": row.get("pert_type", ""),
            "en_src": row.get("en_src", ""),
            "es_tgt": row.get("es_tgt", ""),
        }

        if condition_name == "askqe":
            selected_fields.update({
                "questions": parse_list(row.get("questions", row.get("questions", ""))),
                "ref_answers": parse_list(row.get("ref_answers", row.get("ref_answers", ""))),
                "pred_answers": parse_list(row.get("pred_answers", row.get("pred_answers", ""))),
            })
        elif condition_name == "bt":
            selected_fields.update({
                "backtranslation": row.get("backtranslation", ""),
            })
        elif condition_name == "annotation":
            selected_fields.update({
                "xcomet_annotations": parse_list(row.get("xcomet_annotations", row.get("xcomet_annotations", ""))),
            })
        elif condition_name == "explanation":
            selected_fields.update({
                "explanation": row.get("explanation", ""),
            })

        selected_examples.append(selected_fields)

    print("Sampled IDs (Random):", [e["id"] for e in selected_examples])
    print("Condition:", condition_name)
    print("Length of Selected examples:", len(selected_examples))

    return selected_examples, condition_name


# ---------------------------------Flask App---------------------------------
app = Flask(__name__, static_url_path='/static')
#run_with_ngrok(app)
app.templates_auto_reload = True

RESPONSE_DIR = 'responses'
os.makedirs(RESPONSE_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    save_name = time.strftime("%Y%m%d-%H%M%S")  # Save by date
    if request.method == 'POST':
        try:
            data = request.get_json()
            data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
            if not data:
                return "No response received", 400

            print("Response data: ", data)

            prolific_id = data.get("prolific_id", "unknown")  # Use generated annotator ID
            response_file = os.path.join(RESPONSE_DIR, f'{prolific_id}.csv')
            file_exists = os.path.isfile(response_file)

            fieldnames = [
                "condition", "prolific_id",
                "id", "step", "is_shareable", "is_attention_check", "pert_type", "en_src", "es_tgt",
                "shareability_response", "confidence_response", 
                "first_language", "en_proficiency", "target_proficiency", "mt_frequency",
                "workload", "helpfulness", "trust", "follow_up_12", "follow_up_3", "follow_up_45",
                "timestamp"
            ]

            # Ensure all keys are present in the data
            for field in fieldnames:
                if field not in data:
                    data[field] = ""

            with open(response_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)

            return "Response saved", 200

        except Exception as e:
            print("Error:", str(e))
            return "Error processing request", 500

    else:
        examples, condition = get_examples()
        if examples is None:
            return render_template('error.html')

        return render_template('index.html', examples=examples, condition=condition, target_language='Spanish')
    

@app.route('/end')
def end():
    return render_template('end.html')


if __name__ == "__main__":
    print({key: len([i for i in value if value[i] == 0]) for key, value in samples_tracked.items()})
    app.run(host='0.0.0.0', port=7001)
