import sqlite3
from datetime import datetime

# Connects to the DataBase
conn = sqlite3.connect('System.db', check_same_thread=False)
conn.execute('''CREATE TABLE if not exists Entry_Log 
  (ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Authorised INTEGER,
  User_ID INTEGER,
  DateTime DATETIME)''')
conn.commit()
DateTime = datetime.now()
conn.execute(
    "INSERT INTO Entry_Log(Authorised, DateTime) VALUES (?,?)", (0, DateTime))
conn.commit()
