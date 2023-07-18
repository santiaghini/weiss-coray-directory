import json

DATA_PATH = "data/data.json"
def load_data(path=DATA_PATH):
    with open(path) as f:
        return json.load(f)