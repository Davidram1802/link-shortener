from fastapi import FastAPI,HTTPException,Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from typing import Optional
from hash_function import create_short_link
from datetime import datetime, timezone,timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from model import db, User, UserInDB

SECRET_KEY ='9406c796ef64db9dd08dfb7a681792b7435104293118360b09e6c8d09dd8186a'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

""" fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # sin hash = 'secret'
        "disabled": False,
    }
} """
class Link(BaseModel):
    key: str
    link: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

app = FastAPI()

urls = db.enlaces # coleccion en mongodb que tiene los key-values de los links

users = db.users

# links_dict = get_dict_links(db) # diccionario con key-->url hasheada value-->la url

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_user(db, username: str):
    user = db.find_one({username + '.username': username})
    if user:
        user_dict = user[username]
        print(user,user_dict)
        return UserInDB(**user_dict)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token} 



@app.get("/")
async def get_all(token: str = Depends(oauth2_scheme)): 
    cursor = urls.find()
    salida={}
    for row in cursor:
        salida[row['url_shorted']] = row['url']
    return salida


@app.get('/{url_sorted}') 
async def redirect(url_shorted:str):
    url_to_redirect = urls.find_one({'url_shorted':url_shorted})
    if url_to_redirect is not None:
        del url_to_redirect['_id']
        return {'url_to_redirect':url_to_redirect}
        #return  RedirectResponse(url= url_to_redirect['url'])
    else:
        raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')


@app.post("/addurl/{url}")
async def func(url:str):
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    url_shorted = create_short_link(url,timestamp)
    url = ' http://' + url
    new_url={'url_shorted' : url_shorted} 

    new_url['url'] = url

    urls.insert_one(new_url)

    return new_url 

@app.post('/new_user')
async def add_new_user(username: str, password: str,email: Optional[str] = None,
    full_name: Optional[str] = None, disabled: Optional[bool] = None):
    user_json = {username:{
        "username": username,
        "email": email,
        "full_name": full_name,
        "disabled": disabled,
        "hashed_password":pwd_context.hash(password),
        "urls": []
    }}
    user = UserInDB(**user_json[username])
    users.insert_one({user.username : dict(user)})
    del user_json[username]['hashed_password']
    return user_json

@app.post("/user/addurl/{url}") 
async def add_url_current_user(url,token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token=token)
    user_urls = user.urls
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    nueva_url = {'url_shorted': create_short_link(url,timestamp), 'url':url}
    users.update_one({user.username+'.urls': user_urls},{"$set":{user.username+'.urls': user_urls + [nueva_url]}})
    return nueva_url

@app.get('/user/addurl/{url_shorted}')
async def get_url_current_user(url_shorted,token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token=token)
    url = None
    for url_dict in user.urls:
        if url_dict['url_shorted'] == url_shorted:
            url = url_dict['url']
    if url:
        return {'url':url}
    else: 
        raise HTTPException(status_code=404,detail='The link does not exist, could not redirect.')