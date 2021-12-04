import re
import time
import base64
import sqlite3
from tkinter import *
from datetime import datetime
from functools import partial

conn = sqlite3.connect('System.db', check_same_thread=False)

largeFont= ("Verdana", 12)
normFont = ("Helvetica", 10)
smallFont = ("Helvetica", 8)

def exitAccountCreationWindow(accountCreationWindow):
    accountCreationWindow.destroy()

def closePopUp(accountCreationWindow, popUp):
    popUp.destroy()
    accountCreationWindow.destroy()
    createAccount()

def accountcreationError(message, accountCreationWindow):
    popUp = Tk()
    popUp.geometry('250x100')
    popUp.title('Alert!')
    label = Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command = lambda: [closePopUp(accountCreationWindow, popUp)])
    button.pack()
    popUp.mainloop()

def accountValidation(userName, firstName, lastName, email, password, confirmPassword, adminPrivileges, accountCreationWindow):
    # Retreaving the information from the users inputs for validation
    userName = userName.get()
    firstName = firstName.get()
    lastName = lastName.get()
    email = email.get()
    password = password.get()
    confirmPassword = confirmPassword.get()
    admin = adminPrivileges.get()
    
    # Regex for email validation
    emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in (len(userName), len(firstName), len(lastName), len(email), len(password), len(confirmPassword), len(admin)):
        message = 'Some fields are blank \n Please fill all of them in'
        accountcreationError(message, accountCreationWindow)
        
    
    if len(cursor) == 1:  # Checks that the username is not taken
        message = 'Username is already taken, please try a different one'
        accountcreationError(message, accountCreationWindow)
        
    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        message = 'Email not valid, please try again'
        accountcreationError(message, accountCreationWindow)

    # Checking the password
    if password != confirmPassword:  # Checks that the passwords match
        message = 'Passwords do not match please try again'
        accountcreationError(message, accountCreationWindow)

    if len(password) < 6:  # Checks the length of the password
        message = 'Password is not strong enough \n Please use a minimum of 6 characters'
        accountcreationError(message, accountCreationWindow)

    # Checking if the created user should have admin privileges
    
    adminYes = ['y', 'Y', 'yes', 'YES', 'Yes']
    adminNo = ['n', 'N', 'no', 'NO', 'No']
    
    if admin in adminYes:
        adminPrivileges = 1

    elif admin in adminNo:
        adminPrivileges = 0

    else:
        message = 'Admin privileges not in correct form \n Please try again'
        accountcreationError(message, accountCreationWindow)
        
    # Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()
    
    # Making the characters of the email lowercase
    email = email.lower()

    # Encrypting the password
    password = password.encode("utf-8")
    password = base64.b64encode(password)
    
    conn.execute("INSERT INTO appUsers(userName, hashedPassword, firstName, lastName, email, adminPrivileges, timeCreated) VALUES (?,?,?,?,?,?,?)", [
                 userName, password, firstName, lastName, email, adminPrivileges, timeCreated])  # Writes the information to the db
    conn.commit()
    accountCreationWindow.destroy()    

def createAccount():
    accountCreationWindow = Tk()
    accountCreationWindow.geometry('390x410')
    accountCreationWindow.title('Create account')

    spacer1 = Label(accountCreationWindow, text ="").grid(row=0, column=0)

    userName = StringVar()
    userNameLabel = Label(accountCreationWindow, text="User Name", pady=10, width=22, anchor='w').grid(row=1, column=1)
    userNameEntry = Entry(accountCreationWindow, textvariable=userName, width=30).grid(row=1, column=2)

    firstName = StringVar()
    firstNameLabel = Label(accountCreationWindow, text="First name", pady=10, width=22, anchor='w').grid(row=2, column=1)
    firstNameEntry = Entry(accountCreationWindow, textvariable=firstName, width=30).grid(row=2, column=2)

    lastName = StringVar()
    lastNameLable = Label(accountCreationWindow, text="Last name", pady=10, width=22, anchor='w').grid(row=3, column=1)
    lastNameEntry = Entry(accountCreationWindow, textvariable=lastName, width=30).grid(row=3, column=2)

    email = StringVar()
    emailLable = Label(accountCreationWindow, text="Email", pady=10, width=22, anchor='w').grid(row=4, column=1)
    emailEntry = Entry(accountCreationWindow, textvariable=email, width=30).grid(row=4, column=2)

    password = StringVar()
    passwordLabel = Label(accountCreationWindow, text="Password", pady=10, width=22, anchor='w').grid(row=5, column=1)
    passwordEntry = Entry(accountCreationWindow, textvariable=password, show='*', width=30).grid(row=5, column=2)

    confirmPassword = StringVar()
    confirmPasswordLabel = Label(accountCreationWindow, text="Confirm password", pady=10, width=22, anchor='w').grid(row=6, column=1)
    confirmPasswordEntry = Entry(accountCreationWindow, textvariable=confirmPassword, show='*', width=30).grid(row=6, column=2)

    adminPrivileges = StringVar()
    adminPrivilegesLable = Label(accountCreationWindow, text ="Admin privalges (yes/no)", pady=10, width=22, anchor='w').grid(row=7, column=1)
    adminPrivilegesEntry = Entry(accountCreationWindow, textvariable=adminPrivileges, width=30).grid(row=7, column=2)

    spacer2 = Label(accountCreationWindow, text ="").grid(row=8, column=1)
    validateLogin = partial(accountValidation, userName, firstName, lastName, email, password, confirmPassword, adminPrivileges, accountCreationWindow)
    loginButton = Button(accountCreationWindow, text="           Create account           ", command=validateLogin).grid(row=9, column=2)
    spacer3 = Label(accountCreationWindow, text =" ").grid(row=10, column=2)
    exitButton = Button(accountCreationWindow, text ="             Exit            ", command = lambda: [exitAccountCreationWindow(accountCreationWindow)]).grid(row=11, column=2)
    accountCreationWindow.mainloop()
    
createAccount()