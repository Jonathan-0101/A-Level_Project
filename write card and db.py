#Importing the requiered moduels
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
from datetime import datetime


def dict_factory(Cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return

conn = sqlite3.connect("System.db")  #Connects to the Database
conn.execute("""CREATE TABLE if not exists ID_CARDS 
  (ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Hashed_ID INTEGER,
  Username VARCHAR,
  First_name TEXT,
  Last_name TEXT,
  Time_created DATETIME);""")   #Creates the dable if it does not exist
conn.commit()   #Commits it to the database
#Sets up the GPIO pins and defines the reader
GPIO.setwarnings(False)
reader = SimpleMFRC522()

def writeCard():    #Function for writing the card and db
    #Inputs to get information about the card owner
    text = input("New data:")
    firstName = input("First name: ")
    lastName = input("Last name: ")
    timeCreated = datetime.now()
    print("Now place your tag to write")
    reader.write(text)
    print("Written")
    cardId, text = reader.read()    #Reading the card
    cardId = cardId % 1999  #Hashing the cardId
    print()
    conn.execute(
        "INSERT INTO ID_CARDS(Hashed_ID, text, First_name, Last_name, Time_created) VALUES (?,?,?,?,?)",
        [cardId, text, firstName, lastName, timeCreated],
    )   #Writes the information to the db
    conn.commit()

def readCard(): #Function for reading the card
    print("Hold a tag near the reader")
    ID, text = reader.read()
    print("ID: %s\nText: %s" % (ID, text))
    print()

def menu(): #Menu for the user to choose what they want to do
    choice = input("Do you want to read or write, R for read, W for write: ")
    if choice == "w" or "W":
        writeCard()
        menu()
    elif choice == "r" or "R":
        readCard()
        menu()

menu()
