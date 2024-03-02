from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Message(BaseModel):
    source: str
    destination: str

class QueryResults(Message):
    query_id: int
    num_results: int

class TokenizerResults(Message):
    query_id: int
    tokenizer_json: str

class SearchRequest(Message):
    query: str

class TrainCommand(Message):
    query_id: int
    type: str
    params: dict

class Query(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    url: str

class Sequence(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    text: str
    query_id: Optional[int] = Field(default = None, foreign_key = "query.id")