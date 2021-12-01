import re
import time
import base64
import sqlite3
from datetime import datetime
from os import system, name

#Connects to the DataBase
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

#Regex for email validation
emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def clear():  #Function to clear screen
    if name == 'nt':
        _ = system('cls')

def createAccount():  #Function to create account
    #Getting the information needed
    userName = input("Username: ")
    clear()
    firstName = input("First name: ")
    clear()
    lastName = input("Last name: ")
    clear()
    email = input("Email: ")
    clear()
    confirmEmail = input("Confirm email: ")
    clear()
    password = input("Password: ")
    clear()
    confirmPassword = input("Confirm password: ")
    clear()
    admin = input("Admin privaleges (y/n): ")
    clear()

    now = datetime.now() #Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    
    #Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if len(cursor) == 1:  #Checks that the username is not taken
        print("Username is already taken, please try a different one")
        time.sleep(2)
        clear()
 
    if email != confirmEmail:  #Checks that the emails match
        print("Emails do not match please try again")
        time.sleep(2)
        clear()
        createAccount()

    if not (re.fullmatch(emailCheck, email)):  #Checks against the regex that the email is valid
        print("Email not valid, please try again")
        time.sleep(2)
        clear()
        createAccount()

    #Checking the password
    if password != confirmPassword:  #Checks that the passwords match
        print("Passwords do not match please try again")
        time.sleep(2)
        clear()
        createAccount()

    if len(password) < 6:  #Checks the length of the password
        print("Password is not strong enough")
        print("Please use a minimum of 6 characters")
        time.sleep(2)
        clear()
        createAccount()

    #Checking if the created user should have admin privileges
    if admin == 'y' or 'Y':
        adminPrivileges = 1

    elif admin == 'n' or 'N':
        adminPrivileges = 0

    elif admin != 'y' or 'Y' or 'n' or 'N':
        print("Admin privileges not in correct form please try again")
        time.sleep(2)
        clear()
        createAccount()

    #Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()
    
    #Making the characters of the email lowercase
    email = email.lower()

    #Encrypting the password
    password = password.encode("utf-8")
    password = base64.b64encode(password)
    
    conn.execute("INSERT INTO appUsers(userName, hashedPassword, firstName, lastName, email, adminPrivileges, timeCreated) VALUES (?,?,?,?,?,?,?)", [
                 userName, password, firstName, lastName, email, adminPrivileges, timeCreated])  #Writes the information to the db
    conn.commit()

def menu():
    print('Welcome')
    options = ["Create account", "Exit"]
    counter = 1
    for i in options:
        print(counter, ".", i)
        counter += 1
    response = (input("\n Please select option \n"))
    if response == '1':
        clear()
        createAccount()
        menu()
    if response == '2':
        exit()
    else:
        print("Error please select a valid option")
        time.sleep(2)
        menu()

menu()
