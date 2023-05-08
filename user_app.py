from typing import Union, Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5

items = {
    "foo": dict(name="Foo", price=50.2),
    "bar": dict(name="Bar", description="The Bar fighters", price=62, tax=20.2),
    "baz": dict(name="Baz", description="There goes my baz", price=50.2, tax=10.5),
}

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "descriptor"}
)
async def read_item_name(item_id: str):
    print(items[item_id])
    return items[item_id]

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get(
    "items/{item_id}/public",
    status_code=201,
    response_model=Item,
    response_model_exclude={"tax"}
)
async def read_item_public_data(item_id: str):
    print(items[item_id])
    return items[item_id]


# @app.post("/user/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user

# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Union[str, None] = None
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Union[str, None] = None

# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user
