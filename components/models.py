from pydantic import BaseModel

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