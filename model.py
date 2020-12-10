from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:3306')
db = client['links']

m_link=db.enlaces
example = {
    'vids':'https://youtube.com'
}
m_link.insert_one(example)