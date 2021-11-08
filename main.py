# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, FilePath, DirectoryPath, EmailStr

# Fast Api
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie

class HairColor(Enum):
    white: "white"
    black: "black"
    red: "red"
    blonde: "blonde"

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='James'
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Bond'
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=30
    )
    #hair_color: Optional[HairColor] = Field(default=None, example='white')
    is_married: Optional[bool] = Field(default=None, example='True')
    #photo_file: FilePath(default=None)
    #photo_directory: DirectoryPath(default=None)

    class Config:
        schema_extra = {
            'example': {
                "first_name": "John",
                "last_name": "Parra",
                "age": 34,
                #"hair_color": "black",
                "is_married": True
            }
        }
class Person(PersonBase):
    password: str = Field(
        ..., 
        min_length=1, 
        example="123456"
        )
    class Config:
        schema_extra = {
            'example': {
                "first_name": "John",
                "last_name": "Parra",
                "age": 34,
                #"hair_color": "black",
                "is_married": True,
                "password": "12345689"
            }
        }

class PersonOut(PersonBase):
    pass
class Location(BaseModel):
    city: str
    state: str
    country: str
    class Config:
        schema_extra = {
            'example': {
                "city": "Cajica",
                "state": "Cundinamarca",
                "country": "Colombia"
            }
        }

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="miguel2021"
        )
    message: str = Field(default='Login succesfully!!!')


app = FastAPI()


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"hello": "WORLD"}


@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        title="Name Query",
        description="Name of person from query",
        min_length=1,
        max_length=50,
        example='Alf'
    ),
    age: str = Query(
        ...,
        title="Age Query",
        description="Age of person from query",
        example=456
    )
):
    return {name: age}


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        ge=0,
        example=123
    )
):
    return {person_id: "It exist!"}


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title="person_id",
        description="This is the person_id",
        gt=0,
        example=124
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        example="Pedro"
        ),
    last_name: str = Form(
        ...,
        max_length=20,
        example="Perez"
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent
