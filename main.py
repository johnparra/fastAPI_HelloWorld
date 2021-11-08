# Python
from typing import Optional
from enum import Enum
from fastapi.datastructures import UploadFile

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Fast Api
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form
from fastapi import Header, Cookie, HTTPException, status
from fastapi import UploadFile, File

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
    status_code=status.HTTP_200_OK,
    tags=["Clients"]
    )
def home():
    """
    Title
    Function
    Parameters
    Result
    """
    return {"hello": "WORLD"}


@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create persons from 0"
    )
def create_person(person: Person = Body(...)):
    """
    Title

    Function

    Parameters

    Result
    """
    return person


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show details from person"
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
    """
    Title

    Functionality

    Parameters

    Results
    """
    return {name: age}

persons = [1,2,3,4,5,6,7,8,9]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show details from id person"
    )
def show_person(
    person_id: int = Path(
        ...,
        ge=0,
        example=123
    )
):
    """
    Title

    Functionality

    Parameters

    Results
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!The person_id doesn't exist in this information system"
        )
    return {person_id: "It exist!"}


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
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
    status_code=status.HTTP_200_OK,
    tags=["Persons", "Clients"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Clients"]
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

@app.post(
    path="/post-file",
    status_code=status.HTTP_201_CREATED,
    tags=["Files"]
)
def post_file(
    file: UploadFile = File(...)
):
    return {
        "filename": file.filename,
        "type": file.content_type,
        "size": round(len(file.file.read())/1024, ndigits=2)
    }