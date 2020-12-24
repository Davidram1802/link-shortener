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

user1 ={
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # sin hash = 'secret'
        "urls":[]
    }
}
user_in_db = User(**user1['johndoe'])
print(user_in_db)
# db_users.insert_one(dict(user_in_db))

#db_users.insert_one(user1)
# example = {
#     'url_shorted':'vids',
#     'url':'https://youtube.com'
    
# }
# example2 = {
#     'url_shorted' : 'code',
#     'url':'https://github.com'
# }

print(db.enlaces.find_one({'url_shorted':'code'}))

def get_dict_links(db):
    cursor = db.enlaces.find({})
    m_dict = {}
    for item in cursor: 
        actual_key = list(item.keys())[1]
        m_dict[actual_key] = item[actual_key]
    return m_dict