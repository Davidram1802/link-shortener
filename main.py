from fastapi import FastAPI,HTTPException
#from pydantic import BaseModel
from fastapi.responses import RedirectResponse

# class Item(BaseModel):
#    name:str
#    price:float


app = FastAPI()

urls=[
    {"url":"https://www.instagram.com", "url_shorted": 'insta'},
    {"url":"https://www.youtube.com", "url_shorted":'vids'},
    {"url":"https://www.google.com", "url_shorted":'buscar'}
]

'''
@app.get("/")
async def test(param1,param2):
    return {"parametro1":param1,"parametro2":param2}'''


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get('/{url_shorted}')
async def redirect(url_shorted:str):
    url_to_redirect = None
    for url in urls:
        if url["url_shorted"] == url_shorted:
            url_to_redirect=url["url"]
    if url_to_redirect is not None:
        #response = RedirectResponse(url=url_to_redirect)
        #return response
        # return {'url_to_redirect':url_to_redirect}
        return RedirectResponse(url=url_to_redirect)
    #else:
        # raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')



@app.get("/getall")
async def get_all():
    return urls

@app.post("/addurl/{url}")
async def func(url:int):
    new_url={"url":url, "url_sorted":url.__hash__}
    urls.append(new_url)
    return new_url # hashear la url (cambiar url2 por la funcion de hasheo)