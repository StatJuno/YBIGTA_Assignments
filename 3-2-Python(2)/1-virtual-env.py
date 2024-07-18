import os
import sys
import pickle


PICKLE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/versions.pickle"

def load() -> dict[str, list[str]]:
    try:
        return pickle.load(open(PICKLE_PATH, "rb"))
    except:
        return dict()

def vis(d: dict[str, list[str]]) -> str:
    s = []
    for k, v in d.items():
        s.append(f"{k}")
        for path in v:
            s.append(f"    - {path}")
    return "\n".join(s)


if __name__ == "__main__":
    d = load()
    d[sys.version] = sys.path

    print(f"current: {len(d)}\ndict:\n{vis(d)}")
    if len(d) >= 3:
        print("good!")

    pickle.dump(d, open(PICKLE_PATH, "wb"))
