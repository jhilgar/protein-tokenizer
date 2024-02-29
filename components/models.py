from pydantic import BaseModel

class Message(BaseModel):
    timestamp: str
    source: str

class QueryResults(Message):
    query_id: int
    num_results: int

class SearchRequest(BaseModel):
    url: str