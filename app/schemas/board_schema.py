from pydantic import BaseModel, Field
from typing import Optional

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

class BoardModify(BaseModel):
    title: str
    content: str
    plain_text: str
    name: str|None = None
    pwd: str|None = None
    new_pwd: str|None = None

class BoardSearch(BaseModel):
    name: Optional[str] = None
    toc: Optional[str] = None # title + content
    use: Optional[bool] = None