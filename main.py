from fastapi import FastAPI,HTTPException,Depends
sifrom pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from hash_function import create_short_link
from datetime import datetime, timezone
import redis

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

app = FastAPI()

re = redis.Redis(host='127.0.0.1',port= 6379 ) 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token} 


@app.get("/")
async def get_all():
    keys_list=re.keys()
    keys_values=[{'key':key,'value':re.get(key)} for key in keys_list]
    return keys_values


@app.get('/{url_sorted}')
async def redirect(url_shorted:str):
    url_to_redirect=re.get(url_shorted)
    
    if url_to_redirect is not None:
        # return {'url_to_redirect':url_to_redirect}
        return  RedirectResponse(url= url_to_redirect.decode('utf-8') ,status_code=302)
    else:
        raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')


@app.post("/addurl/{url}")
async def func(url:str):
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    new_url={"url":' http://' + url, "url_shorted":create_short_link(url,timestamp)} # añadir http://

    re.set(new_url['url_shorted'], new_url['url'])

    return new_url 
