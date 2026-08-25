from pydantic import BaseModel, HttpUrl

class CreateRequest(BaseModel):
    original_url: HttpUrl

class CreateResponse(BaseModel):
    id:int
    original_url:str
    short_code:str
    