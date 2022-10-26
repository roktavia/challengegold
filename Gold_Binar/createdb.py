import pandas as pd
import sqlite3
import csv

#Open connection to Database
connection = sqlite3.connect('Gold_Binar.db')

cursor = connection.cursor()

#Create table if not existed yet
cursor.execute('''CREATE TABLE IF NOT EXISTS abusive(abusive TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS data(Tweet TEXT NOT NULL,
HS INTEGER,
Abusive INTEGER,
HS_Individual INTEGER,
HS_Group INTEGER,
HS_Religion INTEGER,
HS_Race INTEGER,
HS_Physical INTEGER,
HS_Gender INTEGER,
HS_Other INTEGER,
HS_Weak INTEGER,
HS_Moderate INTEGER,
HS_Strong INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS new_kamusalay(alay TEXT NOT NULL,
fix_alay TEXT NOT NULL)''')

abusive = pd.read_csv(
    filepath_or_buffer ='/Users/Akbar/Desktop/Gold_Binar/archive/abusive.csv',
    header = 0
)

connection2 = sqlite3.connect('/Users/Akbar/Desktop/Gold_Binar/Gold_Binar.db')

abusive.to_sql(
    name = 'abusive',
    con = connection2,
    if_exists = 'replace',
    index = False,
    dtype ={'abusive': 'text'}
)

data = pd.read_csv(
    filepath_or_buffer ='/Users/Akbar/Desktop/Gold_Binar/archive/data.csv', encoding='latin-1',
    header = 0
)

connection3 = sqlite3.connect('/Users/Akbar/Desktop/Gold_Binar/Gold_Binar.db')

data.to_sql(
    name = 'data',
    con = connection3,
    if_exists = 'replace',
    index = False,
)


new_kamusalay = pd.read_csv(
    filepath_or_buffer ='/Users/Akbar/Desktop/Gold_Binar/archive/new_kamusalay.csv', encoding='latin-1',
    header = 0
)

connection4 = sqlite3.connect('/Users/Akbar/Desktop/Gold_Binar/Gold_Binar.db')

new_kamusalay.to_sql(
    name = 'new_kamusalay',
    con = connection4,
    if_exists = 'replace',
    index = False,
)

connection.commit()
connection.close()