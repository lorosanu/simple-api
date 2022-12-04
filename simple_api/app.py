from typing import Dict
from pydantic import BaseModel, Field, constr, root_validator, ValidationError
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response

# enforce a maximum of 1000 chars per input text
class DocText(constr(max_length=1000)):
    __root__: str

class Document(BaseModel):
    text: DocText = Field(..., description='Document text', example='random text')

async def doc_length(request: Request) -> int:
    try:
        body = Document(**(await request.json()))
    except ValidationError:
        return Response(status_code=422)
    return Response(str(len(body.text)), status_code=200)

app = Starlette(routes=[Route("/doc_length", doc_length, methods=["POST"])])