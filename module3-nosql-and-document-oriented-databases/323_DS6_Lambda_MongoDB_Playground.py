"""
import a sqlite3 rpg database and export it to mongodb
"""

import sqlite3
#import os
#from dotenv import load_dotenv

# os.listdir()

# load the dotenv values
# load_dotenv(verbose=True)
# USER = os.environ.get('user')
# PASSWORD = os.getenv('password')
# print(USER)
# print(PASSWORD)


sl_conn = sqlite3.connect(
    'module3-nosql-and-document-oriented-databases/rpg_db.sqlite3')
sl_curs = sl_conn.cursor()
armory_items = sl_curs.execute('SELECT * FROM armory_item').fetchall()
client = pymongo.MongoClient("mongodb://admin:cvPNB3ENf90t1kB9@cluster0-shard-00-00-k4s0t.mongodb.net:27017,cluster0-shard-00-01-k4s0t.mongodb.net:27017,cluster0-shard-00-02-k4s0t.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

more_docs = []
for ai in armory_items:
    doc = {'sql_index': ai[0],
           'name': ai[1],
           'value': ai[2],
           'weight': ai[3]}
    more_docs.append(doc)

db.test.insert_many(more_docs)
list(db.test.find())
