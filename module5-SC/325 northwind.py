"""
Solution for DS6 325 northwind sprint challenge.
"""
#!/usr/bin/env python3
# coding: utf-8

import sqlite3

sl_conn = sqlite3.connect('northwind_small.sqlite3')
sl_curs = sl_conn.cursor()

# What are the ten most expensive items (per unit price) in the database?
sl_curs.execute(
    'SELECT ProductName FROM Product ORDER BY UnitPrice DESC LIMIT 10;')
print("Top 10 product names from most to least:")
sl_curs.fetchall()

# What is the average age of an employee at the time of their hiring?
# (Hint: a lot of arithmetic works with dates.)
sl_curs.execute('SELECT AVG(HireDate-BirthDate) FROM Employee;')
print(f'Average age of an employee at the time of their hiring: {sl_curs.fetchall()[0][0]:.0f}')

# (Stretch) How does the average age of employee at hire vary by city?
sl_curs.execute(
    'SELECT AVG(HireDate-BirthDate), City FROM Employee GROUP BY City;')
print("Average ages by city:")
sl_curs.fetchall()

# What are the ten most expensive items (per unit price) in the database and their suppliers?
sl_curs.execute("""
        SELECT ProductName, CompanyName
        FROM Product
        INNER JOIN Supplier
        ON Product.SupplierId = Supplier.Id
        ORDER BY UnitPrice DESC
        LIMIT 10;""")
print("Ten most expensive items (per unit price) in the database and their suppliers:")
sl_curs.fetchall()

# What is the largest category (by number of unique products in it)?
sl_curs.execute("""
                SELECT CategoryName, COUNT(DISTINCT ProductName) AS distcount
                FROM Product, Category
                WHERE Product.CategoryId = Category.Id
                GROUP BY CategoryName
                ORDER BY distcount DESC
                LIMIT 1;""")
print("Largest category and number of products in it:", sl_curs.fetchall())

# (Stretch) Who's the employee with the most territories? Use TerritoryId
# (not name, region, or other fields) as the unique identifier for territories.
sl_curs.execute("""
                SELECT FirstName, LastName,
                COUNT(DISTINCT EmployeeTerritory.TerritoryId) AS territories
                FROM Employee
                INNER JOIN EmployeeTerritory
                ON Employee.Id = EmployeeTerritory.EmployeeId
                INNER JOIN Territory
                ON EmployeeTerritory.TerritoryId = Territory.Id
                GROUP BY FirstName, LastName
                ORDER BY territories DESC
                LIMIT 1;""")
print("Employee with most territories:", sl_curs.fetchall())

sl_curs.close()
sl_conn.close()


# Output of file:
# Top 10 product names from most to least:
# [('Côte de Blaye',),
#  ('Thüringer Rostbratwurst',),
#  ('Mishi Kobe Niku',),
#  ("Sir Rodney's Marmalade",),
#  ('Carnarvon Tigers',),
#  ('Raclette Courdavault',),
#  ('Manjimup Dried Apples',),
#  ('Tarte au sucre',),
#  ('Ipoh Coffee',),
#  ('Rössle Sauerkraut',)]
#
#  Average age of an employee at the time of their hiring: 37
#
#  Average ages by city:
# [(29.0, 'Kirkland'),
#  (32.5, 'London'),
#  (56.0, 'Redmond'),
#  (40.0, 'Seattle'),
#  (40.0, 'Tacoma')]
#
#  Ten most expensive items (per unit price) in the database and their suppliers:
# [('Côte de Blaye', 'Aux joyeux ecclésiastiques'),
#  ('Thüringer Rostbratwurst', 'Plutzer Lebensmittelgroßmärkte AG'),
#  ('Mishi Kobe Niku', 'Tokyo Traders'),
#  ("Sir Rodney's Marmalade", 'Specialty Biscuits, Ltd.'),
#  ('Carnarvon Tigers', 'Pavlova, Ltd.'),
#  ('Raclette Courdavault', 'Gai pâturage'),
#  ('Manjimup Dried Apples', "G'day, Mate"),
#  ('Tarte au sucre', "Forêts d'érables"),
#  ('Ipoh Coffee', 'Leka Trading'),
#  ('Rössle Sauerkraut', 'Plutzer Lebensmittelgroßmärkte AG')]
#
#  Largest category and number of products in it: [('Confections', 13)]
#
#  Employee with most territories: [('Robert', 'King', 10)]
