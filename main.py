from fastapi import FastAPI,HTTPException
#from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from hash_function import create_short_link
from datetime import datetime, timezone

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
async def get_all():
    return urls

@app.get('/{url_shorted}')
async def redirect(url_shorted:str):
    url_to_redirect = None
    for url in urls:
        if url["url_shorted"] == url_shorted:
            url_to_redirect=url["url"]
    if url_to_redirect is not None:
        # return {'url_to_redirect':url_to_redirect}
        return RedirectResponse(url=url_to_redirect)
    else:
        raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')


@app.post("/addurl/{url}")
async def func(url:str):
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    new_url={"url":'http://' + url, "url_shorted":create_short_link(url,timestamp)}
    urls.append(new_url)
    return new_url # hashear la url (cambiar url2 por la funcion de hasheo)