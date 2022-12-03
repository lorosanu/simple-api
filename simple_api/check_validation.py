import random
from simple_api.app import Document

# define a random longer length text (can go over the 1000 chars limit)
def _define_random_text(text):
    n = random.randint(1, 100)
    doc_text = text * n
    return ''.join(random.sample(doc_text, len(doc_text)))


def validation():
    print("Define data")
    data = [_define_random_text("This is a random text. ") for _ in range(10000)]

    print("Start processing data")
    for _ in range(10000000):
        for input_text in data:
            try:
                body = Document(text=input_text)
                doc_length = len(body.text)
                print(f"{doc_length} chars")
            except:
                print("> 1000 chars")
                pass
