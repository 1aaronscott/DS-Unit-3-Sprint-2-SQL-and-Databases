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
client = pymongo.MongoClient(
    "mongodb://admin:password@cluster0-shard-00-00-k4s0t.mongodb.net:27017,cluster0-shard-00-01-k4s0t.mongodb.net:27017,cluster0-shard-00-02-k4s0t.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

# test case that adds one table
# more_docs = []
# for ai in armory_items:
#     doc = {'sql_index': ai[0],
#            'name': ai[1],
#            'value': ai[2],
#            'weight': ai[3]}
#     more_docs.append(doc)

# db.test.insert_many(more_docs)
# list(db.test.find())

more_docs = []
table_set = set()
for r in range(0, len(sl_curs.execute('SELECT name from sqlite_master where type= "table";')
                      .fetchall())):
    for c in range(0, len(sl_curs.execute('SELECT name from sqlite_master where type= "table";')
                          .fetchall()[r])):
        string = sl_curs.execute(
            'SELECT name from sqlite_master where type= "table";').fetchall()[r][0]
        table_set.add(string)
table_list = list(table_set)

for cur_table in table_list:
    col_list = []
    # generates a list of columns in current table; assumes second column is the column name
    for r in range(0, len(sl_curs.execute(f'PRAGMA table_info({cur_table});').fetchall())):
        for c in range(0, len(sl_curs.execute(f'PRAGMA table_info({cur_table});').fetchall()[r])):
            string = sl_curs.execute(f'PRAGMA table_info({cur_table});').fetchall()[r][1]
            if string not in col_list:
                col_list.append(string)
    rows = sl_curs.execute(f'SELECT * FROM {cur_table};').fetchall()
    for row in rows:
        for col in col_list:
            doc = {'table': cur_table, 'feature': col,
                   'value': row[col_list.index(col)]}
            more_docs.append(doc)

db.test.insert_many(more_docs)
list(db.test.find())

# While programming for mongodb is easier because fewer commands are
# necessary and the free form nosql structure is more forgiving, as a
# novice I prefer postgres with elephantsql because I can locally craft
# a database and only do a final commit when I'm certain things are the
# way they should be.
