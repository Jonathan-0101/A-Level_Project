import re
import sys
import time
import hashlib
import sqlite3
from datetime import datetime

# Connects to the DataBase
conn = sqlite3.connect('System.db', check_same_thread=False)
conn.execute('''CREATE TABLE if not exists appUsers
  (userName VARCHAR PRIMARY KEY,
  hashedPassword INTEGER,
  firstName TEXT,
  lastName TEXT,
  email VARCHAR,
  adminPrivileges INTEGER,
  timeCreated DATETIME);''')
conn.commit()

# Regex for email validation
emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def createAccount():  # Function to create account
    # Getting the information needed
    userName = input("Username: ")
    firstName = input("First name: ")
    lastName = input("Last name: ")
    email = input("Email: ")
    password = input("Password: ")
    confirmPassword = input("Confirm password: ")
    admin = input("Admin privaleges (y/n): ")

    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")

    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in [len(userName), len(firstName), len(lastName), len(email), len(email), len(password), len(confirmPassword), len(admin)]:
        print("Some fields are blank \nPlease fill them all in")
        time.sleep(2)
        print('\n'*10)
        exit()
    
    if len(cursor) == 1:  # Checks that the username is not taken
        print("Username is already taken \nPlease try a different one")
        time.sleep(2)
        print('\n'*10)
        exit()

    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        print("Email not valid, please try again")
        time.sleep(2)
        print('\n'*10)
        exit()

    # Checking the password
    if password != confirmPassword:  # Checks that the passwords match
        print("Passwords do not match please try again")
        print('\n'*10)
        exit()

    if len(password) < 6:  # Checks the length of the password
        print("Password is not strong enough")
        print("Please use a minimum of 6 characters")
        print('\n'*10)
        exit()

    # Checking if the created user should have admin privileges
    if admin == 'y' or 'Y':
        adminPrivileges = 1

    elif admin == 'n' or 'N':
        adminPrivileges = 0

    elif admin != 'y' or 'Y' or 'n' or 'N':
        print("Admin privileges not in correct form please try again")
        print('\n'*10)
        exit()

    # Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()

    # Making the characters of the email lowercase
    email = email.lower()

    # Encrypting the password
    password = password.encode()
    password = hashlib.sha3_512(password).hexdigest()

    print("Account created sucsesfully")


def menu():
    print('Welcome')
    options = ["Create account", "Exit"]
    counter = 1
    for i in options:
        print(counter, ".", i)
        counter += 1
    response = (input("\n Please select option \n"))
    if response == '1':
        print("\n"*10)
        createAccount()
        print("\n"*10)
        menu()
    if response == '2':
        print()
        sys.exit()
    else:
        print("Error please select a valid option")
        time.sleep(2)
        menu()

menu()
