from typing import Dict
from pydantic import BaseModel, Field, constr, root_validator
from fastapi import FastAPI

# enforce a maximum of 50k chars per input text
class DocText(constr(max_length=50000)):
    __root__: str

class Document(BaseModel):
    text: DocText = Field(..., description='Document text', example='random text')

app = FastAPI()

@app.post("/doc_length")
async def doc_length(body: Document) -> int:
    return len(body.text)