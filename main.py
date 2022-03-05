#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr, HttpUrl, PaymentCardNumber
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Path, Query, Body

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Huamantla"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Tlaxcala"
    ) 
    country: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example="Mexico"
    )

class Person(BaseModel):
    first_name: str = Field(
            ...,
            min_length=1,
            max_length=50
        )
    last_name: str = Field(
            ...,
            min_length=1,
            max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(...)
    web: Optional[HttpUrl] = Field(default=None)
    password: str = Field(..., min_length=8)
    #payment_card: Optional[PaymentCardNumber] = Field(default=None)  

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Francisco",
    #             "last_name": "Lopez Briones",
    #             "age": 38,
    #             "hair_color": "black",
    #             "is_married": False,
    #             "email": "franlopbri@gmail.com",
    #             "password": "password"
    #         }
    #     }

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post("/person/new", 
            response_model=Person,
            response_model_exclude={"password"}
            )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
                    name: Optional[str] = Query(
                            None, 
                            min_length=10, 
                            max_length=50,
                            title="Person Name",
                            description="This is the person name, its between 1 and 50 characters",
                            example="Paco"
                        ),
                    age: Optional[int] = Query(
                            None, 
                            gt=1,
                            title="Person Age",
                            description="The is the person age",
                            example=28
                        )
                ):
    return {"name": name, "age": age}

# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
                    person_id: int = Path(
                            ..., 
                            gt=0,
                            title="Person Id",
                            description="This is the person Id, its greater than 0",
                            example=124
                        )
                ):
    return {person_id: "It exists!"}

# Validaciones Request Body
@app.put("/person/{person_id}")
def update_person(
                    person_id: int = Path(
                        ...,
                        title="Person ID",
                        description="This is the Person ID",
                        gt=0,
                        example=124
                    ),
                    person: Person = Body(...),
                    location: Location = Body(...)
                ):
    results = person.dict()
    results.update(location.dict())
    return results

