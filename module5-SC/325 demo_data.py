"""
Solution to DS6 325 demo data
"""
#!/usr/bin/env python3
# coding: utf-8


import sqlite3

sl_conn = sqlite3.connect('demo_data.sqlite3')
sl_curs = sl_conn.cursor()

create_table = """
                CREATE TABLE demo (
                s VARCHAR(255) PRIMARY KEY,
                x INT,
                y INT);"""

insert_table = """
                INSERT INTO demo
                (s, x, y)
                VALUES
                ('g', 3, 9),
                ('v', 5, 7),
                ('f', 8, 7);"""

sl_curs.execute(create_table)

sl_curs.execute(insert_table)

sl_curs.execute('SELECT * FROM demo;')
sl_curs.fetchall()

sl_curs.execute('SELECT count(*) FROM demo;')
print("Total rows:", sl_curs.fetchall()[0][0])

sl_curs.execute('SELECT COUNT(*) FROM demo WHERE x >= 5 and y >= 5;')
print("Rows where both x and y are at least 5:", sl_curs.fetchall()[0][0])

sl_curs.execute('SELECT COUNT(DISTINCT y) FROM demo;')
print("Unique values of y:", sl_curs.fetchall()[0][0])

sl_curs.close()
sl_conn.commit()
sl_conn.close()

# Output from file:
# Total rows: 3
# Rows where both x and y are at least 5: 2
# Unique values of y: 2
