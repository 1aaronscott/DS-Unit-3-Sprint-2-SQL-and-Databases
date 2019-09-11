# -*- coding: utf-8 -*-
#! python3

"""
Extracts titanic.csv into a sqlite3 database then transforms and loads it into
a postgres instance.
"""

def cursor_connection_close(connection, cursor):
  # function used to close and commit cursors and connections
  cursor.close()
  connection.commit()
  connection.close()

import psycopg2

dbname = 'bhaekzje'
user = 'bhaekzje'
password = 'REMOVED FOR GITHUB'
host = 'salt.db.elephantsql.com'

# cursor_connection_close(pg_conn, pg_curs)

pg_conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host )
pg_curs = pg_conn.cursor()

#column names in titanic.csv:
#Survived,Pclass,Name,Sex,Age,Siblings/Spouses Aboard,Parents/Children Aboard,Fare
create_titanic_table = """
  CREATE TABLE titanic_table (
    id SERIAL NOT NULL PRIMARY KEY, 
    survived INT,
    pclass INT,
    name VARCHAR(255),
    sex TEXT,
    age FLOAT,
    siblings_spouses INT,
    parents_children INT,
    fare FLOAT
);
"""

pg_curs.execute(create_titanic_table)

#code to check that table is empty
#pg_curs.execute('select * from titanic_table;')
#pg_curs.fetchall()

import sqlite3
sl_conn = sqlite3.connect('titanic.sqlite3')
sl_curs = sl_conn.cursor()

import pandas as pd
df = pd.read_csv('titanic.csv')


#for any passengers with a single quote in their names, remove it
df['Name'] = df['Name'].str.replace("'", "")

df.to_sql('titanic', sl_conn, if_exists='replace')

sl_curs = sl_conn.cursor()

passengers = sl_curs.execute('SELECT * FROM titanic;').fetchall()

#data check
#passengers[28]

sl_curs.execute('PRAGMA table_info(titanic);').fetchall()

#load the postgres table with sqlite3 data
for passenger in passengers:
  insert_passenger = """
    INSERT INTO titanic_table
    (id, survived, pclass, name, sex, age, siblings_spouses, parents_children, fare)
    VALUES """ + str(passenger[:]) + ';'
#   print(insert_passenger)
  pg_curs.execute(insert_passenger)

#data check code
#pg_curs.execute('select * from titanic_table;')
#pg_curs.fetchone()

cursor_connection_close(pg_conn, pg_curs)

pg_conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host )
pg_curs = pg_conn.cursor()
pg_curs.execute('SELECT * FROM titanic_table;')
pg_passengers = pg_curs.fetchall()

for passenger, pg_passenger in zip(passengers, pg_passengers):
#   print(passenger, pg_passenger)
  assert passengers == pg_passengers


cursor_connection_close(pg_conn, pg_curs)



