import json

num_conditions = 2

def reset(name):
    data = json.load(open(f'tracker/{name}.json', 'r'))
    for k, v in data.items():
        if v==-1:
            data[k]=0
        elif v<-1:
            data[k]= abs(v+1)
    json.dump(data, open(f'tracker/{name}.json', 'w'), ensure_ascii=False, indent=4)
    
    print(name, len([k for k, v in data.items() if v==1]))
    

for idx in range(1, num_conditions+1):
    data = reset(f'v{idx}')