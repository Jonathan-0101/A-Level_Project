import time
import base64
import sqlite3
import datetime
from tkinter import *
from functools import partial

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

def loginMenu():
    loginWindow = Tk()  
    loginWindow.geometry('400x150')  
    loginWindow.title('Login')
    spacer1 = Label(loginWindow, text ="").grid(row=0, column=0)
    usernameLabel = Label(loginWindow, text="User Name").grid(row=1, column=1)
    username = StringVar()
    usernameEntry = Entry(loginWindow, textvariable=username).grid(row=1, column=2)  
    passwordLabel = Label(loginWindow,text="Password").grid(row=2, column=1)  
    password = StringVar()
    passwordEntry = Entry(loginWindow, textvariable=password, show='*').grid(row=2, column=2)  
    validateLogin = partial(login, username, password, loginWindow)
    loginButton = Button(loginWindow, text="Login", command=validateLogin).grid(row=5, column=1)
    spacer2 = Label(loginWindow, text ="").grid(row=6, column=0)
    loginWindow.mainloop()

def login(username, password, loginWIndow):
    userName = username.get()
    cursor = conn.execute("SELECT * FROM appUsers Where userName = ?",[userName,]).fetchall()
    passwordToCheck = cursor[0][1]
    passwordToEncode = password.get()	
    passwordToEncode = passwordToEncode.encode("utf-8") 
    password = base64.b64encode(passwordToEncode)
    if password == passwordToCheck:
        print("Authorised")
        firstName = cursor[0][2]
        lastName = cursor[0][3]
        email = cursor[0][4]
        adminPrivalges = cursor[0][5]
        if adminPrivalges == 1:
            adminPrivalges = True
            loginWIndow.destroy()
            main(userName, firstName, lastName, email, adminPrivalges)
        else:
            adminPrivalges = False
            loginWIndow.destroy()
            main(userName, firstName, lastName, email, adminPrivalges)
    else:
        print("Unauthorised")

def main(userName, firstName, lastName, email, adminPrivalges):
    print("Username: ", userName)
    print("First name: ", firstName)
    print("Last name: ", lastName)
    print("Email: ", email)
    print("Admin privaleges: ", adminPrivalges)

loginMenu()