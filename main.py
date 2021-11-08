# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# Fast Api
from fastapi import FastAPI, Body, Query, Path


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


class Location(BaseModel):
    city: str
    state: str
    country: str


app = FastAPI()


@app.get("/")
def home():
    return {"hello": "WORLD"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        title="Name Query",
        description="Name of person from query",
        min_length=1,
        max_length=50
    ),
    age: str = Query(
        ...,
        title="Age Query",
        description="Age of person from query"
    )
):
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        ge=0
    )
):
    return {person_id: "It exist!"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="person_id",
        description="This is the person_id",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
