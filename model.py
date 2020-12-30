from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    urls: Optional[list] = []
    
class UserInDB(User):
    hashed_password: str


client = MongoClient('mongodb://127.0.0.1:3306')
db = client['links']

db_links=db.enlaces
db_users = db.users

example = {
    'url_shorted':'vids',
    'url':'https://youtube.com'
    
}
example2 = {
    'url_shorted' : 'code',
    'url':'https://github.com'
}

user1 ={
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "urls":[example,example2],
    }
}
 # hashed_password sin hash = 'secret'
user_in_db = UserInDB(**user1['johndoe'])
# print(user_in_db)
#db_users.insert_one({user_in_db.username:dict(user_in_db)})

# db_users.insert_one(user1)

john = db_users.find_one( {user_in_db.username + '.username' :user_in_db.username})

#print(john)

#print(db.enlaces.find_one({'url_shorted':'code'}))

def get_dict_links(db):
    cursor = db.enlaces.find({})
    m_dict = {}
    for item in cursor: 
        actual_key = list(item.keys())[1]
        m_dict[actual_key] = item[actual_key]
    return m_dict