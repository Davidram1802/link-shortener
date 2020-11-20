from fastapi import FastAPI,HTTPException
#from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from hash_function import create_short_link
from datetime import datetime, timezone
import redis

app = FastAPI()

re = redis.Redis(host='127.0.0.1',port= 6379 ) 


@app.get("/")
async def get_all():
    keys_list=re.keys()
    keys_values=[{'key':key,'value':re.get(key)} for key in keys_list]
    return keys_values

@app.get('/{url_shorted}')
async def redirect(url_shorted:str):
    url_to_redirect=re.get(url_shorted)
    print((url_to_redirect.decode('utf-8')))
    
    if url_to_redirect is not None:
        # return {'url_to_redirect':url_to_redirect}
        return  RedirectResponse(url= url_to_redirect.decode('utf-8') ,status_code=302)
    else:
        raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')


@app.post("/addurl/{url}")
async def func(url:str):
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    new_url={"url": url, "url_shorted":create_short_link(url,timestamp)} # añadir http://

    re.set(new_url['url_shorted'], new_url['url'])

    return new_url 