
import json


def save(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load(path):

    with open(path, "r") as f:
        data = json.load(f)

    return data