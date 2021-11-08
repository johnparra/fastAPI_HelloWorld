#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#Fast Api
from fastapi import FastAPI, Body

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

app = FastAPI()

@app.get("/")
def home():
    return {"hello": "WORLD"}

@app.post("/person/new")
def create_person(person: Person=Body(...)):
    return person