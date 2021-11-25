import sqlite3
import datetime
import time
import re
from os import system, name

conn = sqlite3.connect('System.db', check_same_thread=False) #Connects to the DataBase
conn.execute('''CREATE TABLE if not exists Users 
  (userName VARCHAR PRIMARY KEY,
  hashedPassword INTEGER,
  firstName TEXT,
  lastName TEXT,
  email VARCHAR,
  timeCreated DATETIME);''')
conn.commit()

emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #Regex for email validation

def clear(): #Function to clear screen
    if name == 'nt':
        _ = system('cls')
        
def createAccount(): #Function to create account
    #Getting the information needed
    firstName = input("First name: ")
    clear()
    lastName = input("Last name: ")
    clear()
    userName = input("Username: ")
    clear()
    email = input("Email: ")
    clear()
    confirmEmail = input("Confirm email: ")
    clear()
    password = input("Password: ")
    clear()
    confirmPassword = input("Confirm password: ")
    clear()
    
    if password != confirmPassword: #Checks that the passwords match
        print("Passwords do not match please try again")
        time.sleep(2)
        clear()
        createAccount()
    
    if email != confirmEmail: #Checks that the emails match
        print("Emails do not match please try again")
        time.sleep(2)
        clear()
        createAccount()
        
    if not (re.fullmatch(emailCheck, email)): #Checks against the regex that the email is valid
        print("Email not valid, please try again")
        time.sleep(2)
        clear()
        createAccount()
        
    if len(password) < 6: #Checks the length of the password
        print("Password is not strong enough")
        print("Please use a minimum of 6 characters")
        time.sleep(2)
        clear()
        createAccount()
        
    cursor=conn.execute("SELECT * FROM Users Where userName = ?", [userName]).fetchall() #Searches the database for all instances of the given username
    
    if len(cursor) == 1: #Checks that the username is not taken
        print("Username is already taken, please try a different one")
        time.sleep(2)
        clear()
        createAccount()
        
    toHash = 0
    
    for i in range (len(password)):
        character= password[i]
        asciiCharacterValue = ord(x)
        if toHash == 0:
            toHash = asciiCharacterValue
        else:
            toHash = toHash * asciiCharacterValue
            hashedPassword = toHash %1999    
    
    timeCreated = datetime.now()
    conn.execute("INSERT INTO Users(userName, hashedPassword, firstName, lastName, email, timeCreated) VALUES (?,?,?,?,?,?)", [userName, hashedPassword, firstName, lastName, email, timeCreated]) #Writes the information to the db
    conn.commit()

def menu():
    print('Welcome')
    options = ["Create account", "Exit"]
    counter = 1                       
    for i in options:
        print(counter,".",i)
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