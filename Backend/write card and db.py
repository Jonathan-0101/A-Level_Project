#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys
import sqlite3
from datetime import datetime

def dict_factory(Cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return  

conn = sqlite3.connect('System.db')
conn.execute('''CREATE TABLE if not exists ID_CARDS 
  (ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  Hashed_ID INTEGER NOT NULL,
  Username VARCHAR NOT NULL,
  First_name TEXT NOT NULL,
  Last_name TEXT NOT NULL,
  Time_created DATETIME NOT NULL);''')
conn.commit()

conn.execute('''CREATE TABLE if not exists ENTRY_LOG
  (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  Authorised BOOLEAN NOT NULL,
  USER_ID TEXT NOT NULL,
  DateTime DATETIME NOT NULL);''')
conn.commit()


GPIO.setwarnings(False)



reader = SimpleMFRC522()

while True:
    x=input("Do you want to read or write, R for read, W for write: ")
    if x == 'w':
        text = input('New data:')
        First_name = input('First name: ')
        Last_name = input('Last name: ')
        Time_created = datetime.now()
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
        Card_id, text = reader.read()
        Card_id = Card_id % 1999
        print()
        conn.execute("INSERT INTO ID_CARDS(Hashed_ID, text, First_name, Last_name, Time_created) VALUES (?,?,?,?,?)", [Card_id, text, First_name, Last_name, Time_created]).lastrowid
        conn.commit()
    elif x == 'r':
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        print()
        id, text = reader.read()
        print()
