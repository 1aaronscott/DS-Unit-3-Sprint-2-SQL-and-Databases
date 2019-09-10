#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import sqlite3
import os

# ## Assignment - Part 1, Querying a Database
# - How many total Characters are there?
# - How many of each specific subclass?
# - How many total Items?
# - How many of the Items are weapons? How many are not?
# - How many Items does each character have? (Return first 20 rows)
# - How many Weapons does each character have? (Return first 20 rows)
# - On average, how many Items does each Character have?
# - On average, how many Weapons does each character have?


os.listdir()


conn = sqlite3.connect('rpg_db.sqlite3')


curs = conn.cursor()


character_count = 'SELECT COUNT(name) FROM charactercreator_character;'


# total characters
print(curs.execute(character_count).fetchall())


print(curs.fetchall())


conn.commit()
conn.close()


# total for each class
subclasses = ['cleric', 'fighter', 'mage', 'necromancer', 'thief']
conn = sqlite3.connect('rpg_db.sqlite3')
for subclass in subclasses:
    curs = conn.cursor()
    if subclass == 'necromancer':
        class_count = 'SELECT COUNT(mage_ptr_id) FROM charactercreator_' + \
            subclass+';'
    else:
        class_count = 'SELECT COUNT(character_ptr_id) FROM charactercreator_' + \
            subclass+';'
    print(f'{subclass}: ', curs.execute(class_count).fetchall()[0])
conn.commit()
conn.close()


# total items
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
item_count = 'SELECT count(item_id) from armory_item'
print("total armory items", curs.execute(item_count).fetchall()[0])
conn.close()


# total weapons
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
weapon_count = 'SELECT count(item_ptr_id) from armory_weapon'
print("total armory weapons", curs.execute(weapon_count).fetchall()[0])
conn.close()


# items not weapons
174-37


# counting the number of items each character has (first 20 rows)
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
item_count = 'SELECT character_id, count(id) from\
              charactercreator_character_inventory GROUP by character_id LIMIT 20'
print("total items by character", curs.execute(item_count).fetchall())
conn.close()


# counting the number of weapons each character has (first 20 rows)
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
item_count = 'SELECT character_id, count(item_ptr_id) from\
              charactercreator_character_inventory, armory_weapon, armory_item\
              WHERE armory_weapon.item_ptr_id = armory_item.item_id\
              GROUP by character_id LIMIT 20'
print("total weapons by character", curs.execute(item_count).fetchall())
conn.close()


# On average, how many items each character has
# must use count(character_id) as ci then take avg(ci)
# instead of avg(count(character_id)) even though it is allowed
# in other sql implementations
# https://database.guide/avg-calculate-the-average-value-of-a-column-in-mysql/
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
avg_items = 'SELECT avg(ci) FROM (\
             SELECT *, count(character_id) as ci\
             FROM armory_item, charactercreator_character_inventory\
             WHERE armory_item.item_id = charactercreator_character_inventory.item_id\
             GROUP by character_id)'
print("average items by character", curs.execute(avg_items).fetchall())
conn.close()


# On average, how many Weapons each character has
conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()
avg_weapons = 'SELECT avg(ci) FROM (\
               SELECT *, count(character_id) as ci\
               FROM armory_item, armory_weapon, charactercreator_character_inventory\
               WHERE armory_item.item_id = armory_weapon.item_ptr_id AND armory_item.item_id\
               = charactercreator_character_inventory.item_id\
               GROUP by character_id)'
print("average weapons by character", curs.execute(avg_weapons).fetchall())
conn.close()


# ## Assigment - Part 2, Making and populating a Database
#
# Load the data (use `pandas`) from the provided file `buddymove_holidayiq.csv`
# (the [BuddyMove Data
# Set](https://archive.ics.uci.edu/ml/datasets/BuddyMove+Data+Set)) - you should
# have 249 rows, 7 columns, and no missing values. The data reflects the number of
# place reviews by given users across a variety of categories (sports, parks,
# malls, etc.).
#
# Using the standard `sqlite3` module:
#
# - Open a connection to a new (blank) database file `buddymove_holidayiq.sqlite3`
# - Use `df.to_sql`
#   ([documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html))
#   to insert the data into a new table `review` in the SQLite3 database
#
# Then write the following queries (also with `sqlite3`) to test:
#
# - Count how many rows you have - it should be 249!
# - How many users who reviewed at least 100 `Nature` in the category also
#   reviewed at least 100 in the `Shopping` category?
# - (*Stretch*) What are the average number of reviews for each category?
#


df = pd.read_csv('buddymove_holidayiq.csv')


df.shape


df.isnull().sum()


df.head()


conn = sqlite3.connect('buddymove_holidayiq.sqlite3')


df.to_sql('review', conn)


curs = conn.cursor()


row_count = 'SELECT COUNT([User Id]) FROM review;'


print("Total number of rows: ", curs.execute(row_count).fetchall())


big_nature_shopping = 'SELECT COUNT([User Id]) FROM review WHERE (Nature >= 100) and (Shopping >= 100);'


print("At least 100 Nature and 100 Shopping reviews: ",
      curs.execute(big_nature_shopping).fetchall())


# average for each category
categories = ['Sports', 'Religious', 'Nature', 'Theatre', 'Shopping', 'Picnic']
for cat in categories:
    curs = conn.cursor()
    avg_cat = 'SELECT avg('+cat+') FROM review;'
    print(f'{cat}: ', curs.execute(avg_cat).fetchall()[0])
conn.commit()
conn.close()
