import json
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient('mongodb://127.0.0.1:3306')
db = client['links']

db_links=db.enlaces
example = {
    'vids':'https://youtube.com'
    
}
example2 = {
    'code':'https://github.com'
    
}

def get_dict_links(db):
    cursor = db.enlaces.find({})
    m_dict = {}
    for item in cursor: 
        actual_key = list(item.keys())[1]
        m_dict[actual_key] = item[actual_key]
    return m_dict