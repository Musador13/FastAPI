from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from typing_extensions import Annotated

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()


# @app.post("/files/")
# async def create_file(file: Annotated[
#         bytes | None, File(description="A file read as bytes")] = None):
#     if file:
#         return {"file_size": len(file)}
#     else:
#         return {"message": "No file sent"}
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: Annotated[
#         UploadFile | None, File(description="A file read as UploadFile")] = None):
#     if file:
#         return {"filename": file.filename}
#     else:
#         return {"message": "No upload file sent"}

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/files/")
async def create_files(
    files: Annotated[List[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        List[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

items = {"foo": "The Foo Wrestlers"}

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

@app.post("/items/",
          response_model=Item,
          summary="Create an item",
          response_description="The created item"
          )
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
