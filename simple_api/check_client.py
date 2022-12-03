import random
from fastapi.testclient import TestClient

from simple_api.app import app

# define a random longer length text (can go over the 1000 chars limit)
def _define_random_text(text):
    n = random.randint(1, 100)
    doc_text = text * n
    return ''.join(random.sample(doc_text, len(doc_text)))

def client():
    print("Define data")
    data = [_define_random_text("This is a random text. ") for _ in range(10000)]

    print("Define client")
    client = TestClient(app)

    print("Start processing data")
    for _ in range(10000000):
        for input_text in data:
            try:
                doc_length = client.post("/doc_length", json={"text": input_text})
                print(f"{doc_length} chars")
            except:
                print("> 1000 chars")
                pass