from datetime import datetime, time, timedelta
from enum import Enum
from typing import Annotated, Union, List, Set, Dict, Any
from uuid import UUID

from fastapi import Body, FastAPI, Path, Query, Cookie
from typing_extensions import Annotated
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str = "name"
    description: str | None = Field(
        default=None,
        title="The description of the item",
        min_length=0,
        max_length=100,
    )
    price: float = Field(
        default=100,
        gt=0,  # greater than
        lt=1000,  # less than
        title="The price of the item",
        description="The price must be greater than 0 and less than 1000"
    )
    tax: float | None = None
    tags: Set[str] = set()
    images: List[Image] | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "some name",
                "description": "A very nice Item",
                "price": 13.2,
                "tax": 3.2,
                "tags": ("item", "red",),
                "images": [{"url": "link", "name": "pic"},
                           {"url": "link2", "name": "pic2"}],
            }
        }

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: List[Item]

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

some_item = {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

@app.post("/images/multiple/", response_model=List[Image])
async def create_multiple_images(images: List[Image]) -> Any:
    return images

@app.post("/offers/")
async def create_offer(offer: Offer) -> Offer:
    return offer

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[Union[datetime, None], Body()] = None,
    end_datetime: Annotated[Union[datetime, None], Body()] = None,
    repeat_at: Annotated[Union[time, None], Body()] = None,
    process_after: Annotated[Union[timedelta, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
#
# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: Annotated[int, Path(title="The ID of item", ge=0, le=100)],
#         importance: Annotated[int, Body(gt=0)],
#         item: Annotated[Item, Body(embed=True)],
#         q: Union[str, None] = None,
#         user: Union[User, None] = None,
# ):
#     results = {"item_id": item_id, "importance": importance}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     if user:
#         results.update({"user": user})
#     return results

# async def create_item(item_id: int, item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.tax + item.price
#         item_dict.update({"price_with_tax": price_with_tax})
#     return {"item_id": item_id, **item}


# @app.get("/items/")
# # (q: Union[str, None] = Query(default=None, max_length=50)) old version
# async def read_items(
#         q: Annotated[
#             List[str],
#             Query(
#                 alias="item-query",
#                 title="Query",
#                 description="List of query",
#                 example="",
#                 deprecated=True,
#                 include_in_schema=True,
#             ),
#         ] = ("foo", "bar")):
#
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     query_items = {"q": q}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/item/{item_id}")
# async def read_item(
#         item_id: Annotated[int, Path(title="The id of item")],
#         q: Annotated[Union[str, None], Query(alias="item-query")] = None
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#         return results


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     print(item_id)
#     return {"item_id": item_id}

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "msg": "hi1"}
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "msg": "hi2"}
#
#     return {"model_name": model_name, "msg": "hi3"}
