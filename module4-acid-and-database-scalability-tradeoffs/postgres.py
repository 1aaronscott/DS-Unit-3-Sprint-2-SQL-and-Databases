"""
Exploratory file to answer assignment questions using the postgres
instance and titanic dataset uploaded on 322.
"""
import psycopg2

dbname = 'user'
user = 'user'
password = 'password'
host = 'salt.db.elephantsql.com'

pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
pg_curs = pg_conn.cursor()


def cursor_connection_close(connection, cursor):
    cursor.close()
    # connection.commit()
    connection.close()

# columns names: survived, pclass, name, sex, age, siblings_spouses, parents_children, fare
# How many passengers survived, and how many died?


sql_com1 = """
            SELECT survived, COUNT(*) 
            FROM titanic_table 
            GROUP BY survived
            ORDER BY survived DESC;"""
pg_curs.execute(sql_com1)
rows1 = pg_curs.fetchall()
rows_result1 = [r[1] for r in rows1]
labels1 = ['survived', 'died']
for label, row in zip(labels1, rows_result1):
    print(f'Passengers who {label}: {row}')

# How many passengers were in each class?

sql_com2 = """
            SELECT pclass, COUNT(*) 
            FROM titanic_table 
            GROUP BY pclass
            ORDER BY pclass ASC;"""
pg_curs.execute(sql_com2)
rows2 = pg_curs.fetchall()
rows_result2 = [r[1] for r in rows2]
labels2 = ['1st class', '2nd class', '3rd class']
for label, row in zip(labels2, rows_result2):
    print(f'Passengers in {label}: {row}')

# How many passengers survived/died within each class?

sql_com3 = """
            SELECT pclass, survived, COUNT(*) 
            FROM titanic_table 
            GROUP BY pclass, survived
            ORDER BY survived DESC, pclass ASC;"""
pg_curs.execute(sql_com3)
rows3 = pg_curs.fetchall()
rows_result3 = [r[2] for r in rows3]
labels3 = ['1st class who lived', '2nd class who lived',
           '3rd class who lived', '1st class who died', '2nd class who died',
           '3rd class who died']
for label, row in zip(labels3, rows_result3):
    print(f'{label}: {row}')

# What was the average age of survivors vs nonsurvivors?

sql_com4 = """
            SELECT AVG(age), survived
            FROM titanic_table 
            GROUP BY survived
            ORDER BY survived DESC;"""
pg_curs.execute(sql_com4)
rows4 = pg_curs.fetchall()
rows_result4 = [r[0] for r in rows4]
labels4 = ['survivors', 'nonsurvivors']
for label, row in zip(labels4, rows_result4):
    print(f'Average age of {label}: {row:.0f}')

# What was the average age of each passenger class?

sql_com5 = """
            SELECT AVG(age), pclass
            FROM titanic_table 
            GROUP BY pclass
            ORDER BY pclass ASC;"""
pg_curs.execute(sql_com5)
rows5 = pg_curs.fetchall()
rows_result5 = [r[0] for r in rows5]
labels5 = ['1st class', '2nd class', '3rd class']
for label, row in zip(labels5, rows_result5):
    print(f'Average age of {label}: {row:.0f}')

# What was the average fare by passenger class? By survival?

sql_com6 = """
            SELECT AVG(fare), pclass
            FROM titanic_table 
            GROUP BY pclass
            ORDER BY pclass ASC;"""
pg_curs.execute(sql_com6)
rows6 = pg_curs.fetchall()
rows_result6 = [r[0] for r in rows6]
labels6 = ['1st class', '2nd class', '3rd class']
for label, row in zip(labels6, rows_result6):
    print(f'Average fare {label}: ${row:.2f}')

sql_com7 = """
            SELECT AVG(fare), survived
            FROM titanic_table 
            GROUP BY survived
            ORDER BY survived ASC;"""
pg_curs.execute(sql_com7)
rows7 = pg_curs.fetchall()
rows_result7 = [r[0] for r in rows7]
labels7 = ['nonsurvivors', 'survivors']
for label, row in zip(labels7, rows_result7):
    print(f'Average fare of {label}: ${row:.2f}')

# How many siblings/spouses aboard on average, by passenger class? By survival?

sql_com8 = """
            SELECT AVG(siblings_spouses), pclass
            FROM titanic_table 
            GROUP BY pclass
            ORDER BY pclass ASC"""
pg_curs.execute(sql_com8)
rows8 = pg_curs.fetchall()
rows_result8 = [r[0] for r in rows8]
labels8 = ['1st class', '2nd class', '3rd class']
for label, row in zip(labels8, rows_result8):
    print(f'Average no. of siblings/spouses in {label}: {row:.2f}')


sql_com9 = """
            SELECT AVG(siblings_spouses), survived
            FROM titanic_table 
            GROUP BY survived
            ORDER BY survived ASC"""
pg_curs.execute(sql_com9)
rows9 = pg_curs.fetchall()
rows_result9 = [r[0] for r in rows9]
labels9 = ['died', 'lived']
for label, row in zip(labels9, rows_result9):
    print(f'Average no. of siblings/spouses when people {label}: {row:.2f}')

# How many parents/children aboard on average, by passenger class? By survival?

sql_com10 = """
            SELECT AVG(parents_children), pclass
            FROM titanic_table 
            GROUP BY pclass
            ORDER BY pclass ASC"""
pg_curs.execute(sql_com10)
rows10 = pg_curs.fetchall()
rows_result10 = [r[0] for r in rows10]
labels10 = ['1st class', '2nd class', '3rd class']
for label, row in zip(labels10, rows_result10):
    print(f'Average no. of parents/children aboard for {label}: {row:.2f}')

sql_com11 = """
            SELECT AVG(parents_children), survived
            FROM titanic_table 
            GROUP BY survived
            ORDER BY survived ASC"""
pg_curs.execute(sql_com11)
rows11 = pg_curs.fetchall()
rows_result11 = [r[0] for r in rows11]
labels11 = ['died', 'lived']
for label, row in zip(labels11, rows_result11):
    print(f'Average no. of parents/children when people {label}: {row:.2f}')

# Do any passengers have the same name?

# First create a table that splits the names and keeps only the first name
# Second create a table the counts the first names
# Third create a table that sums the values from table 2
# https://w3resource.com/PostgreSQL/split_part-function.php
sql_com12 = """
            SELECT SUM(total.ct) 
            FROM
                (SELECT fn.first_name, COUNT(*) AS ct
                FROM 
                    (SELECT split_part(name, ' ', 2) AS first_name
                    FROM titanic_table) as fn
                GROUP BY fn.first_name
                HAVING COUNT(*) >= 2) as total"""
pg_curs.execute(sql_com12)
rows12 = pg_curs.fetchall()
for row in rows12:
    print(f'Number of people with the same first name: {row[0]}')


cursor_connection_close(pg_conn, pg_curs)

# Passengers who survived: 342
# Passengers who died: 545
# Passengers in 1st class: 216
# Passengers in 2nd class: 184
# Passengers in 3rd class: 487
# 1st class who lived: 136
# 2nd class who lived: 87
# 3rd class who lived: 119
# 1st class who died: 80
# 2nd class who died: 97
# 3rd class who died: 368
# Average age of survivors: 28
# Average age of nonsurvivors: 30
# Average age of 1st class: 39
# Average age of 2nd class: 30
# Average age of 3rd class: 25
# Average fare 1st class: $84.15
# Average fare 2nd class: $20.66
# Average fare 3rd class: $13.71
# Average fare of nonsurvivors: $22.21
# Average fare of survivors: $48.40
# Average no. of siblings/spouses in 1st class: 0.42
# Average no. of siblings/spouses in 2nd class: 0.40
# Average no. of siblings/spouses in 3rd class: 0.62
# Average no. of siblings/spouses when people died: 0.56
# Average no. of siblings/spouses when people lived: 0.47
# Average no. of parents/children aboard for 1st class: 0.36
# Average no. of parents/children aboard for 2nd class: 0.38
# Average no. of parents/children aboard for 3rd class: 0.40
# Average no. of parents/children when people died: 0.33
# Average no. of parents/children when people lived: 0.46
# Number of people with the same first name: 574
