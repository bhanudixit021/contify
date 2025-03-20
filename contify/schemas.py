from pydantic import BaseModel


class Document(BaseModel):
    id: str
    title: str
    data: str

class SearchResponse(BaseModel):
    id: str
    title: str
    data: str
    score: float

class NoDataResponse(BaseModel):
    message:str