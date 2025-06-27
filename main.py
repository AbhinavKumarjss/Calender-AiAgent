from fastapi import FastAPI,Response,status
from pydantic import BaseModel

app = FastAPI()
class Blog(BaseModel):
    number: int
    body : str

@app.post('/blog/{id}')
def index(id:int,request:Blog , response:Response):
    response.status_code = status.HTTP_201_CREATED;
    return {'Blog' : request} 