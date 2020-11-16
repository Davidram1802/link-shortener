from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name:str
    price:float


app = FastAPI()

urls=[]

@app.get("/")
async def test(param1,param2):
    return {"parametro1":param1,"parametro2":param2}

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/getall")
async def get_all():
    return urls

@app.post("/addurl/{url}")
async def func(url:int, item:Item):
    new_url={"url":url, "url_sorted":item.name}
    urls.append(new_url)
    return new_url # hashear la url (cambiar url2 por la funcion de hasheo)