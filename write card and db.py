# Importing the requiered moduels
import os
import sys
import mariadb
import RPi.GPIO as GPIO
from datetime import datetime
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522

load_dotenv()
dbIp = os.getenv("dbIp")
dbUserName = os.getenv('dbUserName')
dbPassword = os.getenv('dbPassword')

cur = mariadb.connect(host=dbIp, database='iSpy', user=dbUserName, password=dbPassword)

conn = cur.cursor()

# Sets up the GPIO pins and defines the reader
GPIO.setwarnings(False)
reader = SimpleMFRC522()


def writeCard():    # Function for writing the card and db
    # Inputs to get information about the card owner
    text = input("Card name: ")
    firstName = input("First name: ")
    lastName = input("Last name: ")
    timeCreated = datetime.now()
    print("Now place your tag to write")
    reader.write(text)
    print("Written")
    cardId, text = reader.read() # Reading the card
    print()
    conn.execute("INSERT INTO idCards(cardId, cardName, firstName, lastName, active, timeCreated) VALUES (?,?,?,?,?,?)",
                 (cardId, text, firstName, lastName, 1, timeCreated,))
    cur.commit()


def readCard(): # Function for reading the card
    print("Hold a tag near the reader")
    cardId, text = reader.read()
    print("ID: %s\nText: %s" % (cardId, text))
    print()


def menu(): # Menu for the user to choose what they want to do
    choice = input("Do you want to read or write, R for read, W for write: ")

    if choice in ("w", "W"):
        writeCard()
        menu()

    elif choice in ("r", "R"):
        readCard()
        menu()

    else:
        print("Error please try again")
        sys.exit()


menu()
