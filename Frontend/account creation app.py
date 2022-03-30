import os
import re
import ssl
import string
import random
import sqlite3
import smtplib
import hashlib
from tkinter import *
import tkinter as tk
from datetime import datetime
from functools import partial
from dotenv import load_dotenv

conn = sqlite3.connect('database.db', check_same_thread=False)

largeFont= ("Verdana", 12)
normFont = ("Helvetica", 10)
smallFont = ("Helvetica", 8)


def closeWindow(currentWindow):
    currentWindow.destroy()


def popUpWindow(title, message, window):
    popUp = tk.Toplevel(window)
    popUp.geometry('250x100')
    currentWindow = popUp
    popUp.title(title)
    label = Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command=lambda:[closeWindow(currentWindow)])
    button.pack()
    popUp.mainloop()


def emailUser(email, userName, password):
    load_dotenv()

    gmail_user = os.getenv('emailAccount')
    gmail_password = os.getenv('emailPassword')

    userName = 'Jonathan Woolf'

    to = [email]
    subject = 'iSpy'
    body = """\
    An account has just been created for you on iSpy!
    Your username is: """ + userName + """
    Your password is: """ + password + """
    You must change your password after logging in.
    """

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, to, email_text)
        smtp_server.close()

    except Exception as ex:
        print("Something went wrong….",ex)

def accountValidation(acUserName, acFirstName, acLastName, acEmail, acAdminPrivileges, accountCreationWindow, window):
    # Retreaving the information from the users inputs for validation
    userName = acUserName.get()
    firstName = acFirstName.get()
    lastName = acLastName.get()
    email = acEmail.get()
    adminPrivileges = acAdminPrivileges.get()
    title = "Account Creation Error"

    # Regex for email validation
    emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    logInTimeForDB = now.strftime("%d/%m/%Y")

    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in (len(userName), len(firstName), len(lastName), len(email)):
        message = 'Some fields are blank \n Please fill all of them in'
        popUpWindow(title, message, window)

    if len(cursor) == 1:  # Checks that the username is not taken
        message = 'Username is already taken, please try a different one'
        popUpWindow(title, message, window)

    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        message = 'Email not valid, please try again'
        popUpWindow(title, message, window)

    # Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()

    # Making the characters of the email lowercase
    email = email.lower()
    
    # Generating a random password
    passwordToSend = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

    # Encrypting the password
    password = passwordToSend.encode()
    password = hashlib.sha3_512(password).hexdigest()

    emailUser(email, userName, passwordToSend)
    
    conn.execute("INSERT INTO appUsers(userName, hashedPassword, firstName, lastName, email, adminPrivileges, timeCreated, lastLogIn) VALUES (?,?,?,?,?,?,?,?)", [
                 userName, password, firstName, lastName, email, adminPrivileges, timeCreated, logInTimeForDB])  # Writes the information to the db
    conn.commit()
    accountCreationWindow.destroy() 
    title = "Alert!"
    message = "User created successfully"
    popUpWindow(title, message, window)

def createAccount(window):
    accountCreationWindow = tk.Toplevel(window)
    accountCreationWindow.geometry('390x350')
    accountCreationWindow.title('Create account')
    currentWindow = accountCreationWindow

    spacer1 = Label(accountCreationWindow, text="").grid(row=0, column=0)

    acUserName = StringVar()
    userNameLabel = Label(accountCreationWindow, text="User Name", pady=10, width=22, anchor='w').grid(row=1, column=1)
    userNameEntry = Entry(accountCreationWindow, textvariable=acUserName, width=30).grid(row=1, column=2)

    acFirstName = StringVar()
    firstNameLabel = Label(accountCreationWindow, text="First name", pady=10, width=22, anchor='w').grid(row=2, column=1)
    firstNameEntry = Entry(accountCreationWindow, textvariable=acFirstName, width=30).grid(row=2, column=2)

    acLastName = StringVar()
    lastNameLable = Label(accountCreationWindow, text="Last name", pady=10, width=22, anchor='w').grid(row=3, column=1)
    lastNameEntry = Entry(accountCreationWindow, textvariable=acLastName, width=30).grid(row=3, column=2)

    acEmail = StringVar()
    emailLable = Label(accountCreationWindow, text="Email", pady=10, width=22, anchor='w').grid(row=4, column=1)
    emailEntry = Entry(accountCreationWindow, textvariable=acEmail, width=30).grid(row=4, column=2)

    acAdminPrivileges = IntVar()
    adminLable = Label(accountCreationWindow, text="Admin privlages", pady=10, width=22, anchor='w').grid(row=5, column=1)
    Checkbutton(accountCreationWindow, text="                                                       ", variable=acAdminPrivileges).grid(row=5, column=2)

    spacer2 = Label(accountCreationWindow, text="").grid(row=6, column=1)
    loginButton = Button(accountCreationWindow, text="           Create account           ", command=lambda:[accountValidation(acUserName, acFirstName, acLastName, acEmail, acAdminPrivileges, accountCreationWindow, window)]).grid(row=7, column=2)
    spacer3 = Label(accountCreationWindow, text=" ").grid(row=8, column=2)
    exitButton = Button(accountCreationWindow, text="             Exit            ", command=lambda:[closeWindow(currentWindow)]).grid(row=9, column=2)
    accountCreationWindow.mainloop()


window = tk.Tk()
createAccount(window)
window.mainloop()
