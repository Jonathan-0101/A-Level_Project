import os
import time
import sqlite3

from datetime import datetime


conn = sqlite3.connect('database.db', check_same_thread=False) # Connects to the Database

conn.execute('DROP TABLE idCards')
conn.commit()

conn.execute('''CREATE TABLE if not exists idCards 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  cardId INTEGER,
  cardName VARCHAR,
  firstName TEXT,
  lastName TEXT,
  active INTEGER,
  timeCreated DATETIME
  )''')

conn.commit()