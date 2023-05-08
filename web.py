from typing import Union

from fastapi import Depends, FastAPI, Cookie
from typing_extensions import Annotated

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# first level nested dependency
def query_extractor(q: Union[str, None] = None):
    return q

# second level nested dependency
def query_or_cookie_extractor(
        q: Annotated[str, Depends(query_extractor)],
        last_query: Annotated[Union[str, None], Cookie()] = None
):
    if not q:
        return last_query
    return q

# third level nested dependency
@app.get("/tools/")
async def read_query(
        query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}

# Dependency injection with class CommonQueryParams
class CommonQueryParams:
    def __int__(self,
                q: Union[str, None] = None,
                skip: int = 0,
                limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# Dependency Injection with func common_parameters
async def common_parameters(
        q: Union[str, None] = None,
        skip: int = 0,
        limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_parameters)]
CommonsDepClass = Annotated[CommonQueryParams, Depends(CommonQueryParams)]

@app.get("/items/")
async def read_items(commons: CommonsDepClass):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
        items = fake_items_db[commons.skip : commons.skip + commons.limit]
        response.update({"items": items})
        return response

# @app.get("/items/")
# async def read_items(commons: CommonsDep):
#     return commons

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
