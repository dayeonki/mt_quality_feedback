import json

total_examples = 20
conditions = ["askqe", "bt", "annotation", "explanation"]

for condition in conditions:
    examples = {i:0 for i in range(1, total_examples+1)}
    json.dump(examples, open(f'tracker/{condition}.json', 'w'), ensure_ascii=False, indent=4)


with open('tracker/last_condition.txt', 'w') as f:
    f.write('0')