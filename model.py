from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:3306')
db = client['links']

db_links=db.enlaces
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