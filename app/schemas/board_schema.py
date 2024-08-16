from pydantic import BaseModel, Field

class BoardDetails(BaseModel):
    seq_board: int
    title: str
    content_summary: str|None = None
    name: str|None = None

class BoardAdd(BaseModel):
    title: str
    content: str
    plain_text: str
    name: str|None = None
    pwd: str|None = None

class BoardSearch(BaseModel):
    name: str|None = None
    toc: str|None = None # title + content
    use: bool|None = None