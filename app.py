import time
import base64
import sqlite3
from tkinter import *
from datetime import datetime
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

largeFont= ("Verdana", 12)
normFont = ("Helvetica", 10)
smallFont = ("Helvetica", 8)

def loginMenu():
  loginWindow = Tk()
  loginWindow.geometry('330x195')
  loginWindow.title('Login')
  currentWindow = loginWindow
  spacer1 = Label(loginWindow, text ="").grid(row=0, column=0)
  username = StringVar()
  usernameLabel = Label(loginWindow, text="User Name", pady=10, width=10, anchor='w').grid(row=1, column=1)
  usernameEntry = Entry(loginWindow, textvariable=username,  width=30).grid(row=1, column=2)
  password = StringVar()
  passwordLabel = Label(loginWindow, text="Password", pady=10, width=10, anchor='w').grid(row=2, column=1)
  passwordEntry = Entry(loginWindow, textvariable=password, show='*',  width=30).grid(row=2, column=2)
  validateLogin = partial(login, username, password, loginWindow)
  loginButton = Button(loginWindow, text="           Login           ", command=validateLogin).grid(row=3, column=2)
  spacer2 = Label(loginWindow, text =" ").grid(row=4, column=2)
  exitButton = Button(loginWindow, text ="             Exit            ", command = exit).grid(row=5, column=2)
  spacer3 = Label(loginWindow, text ="").grid(row=3, column=0)
  loginWindow.mainloop()

def login(username, password, loginWindow):
  userName = username.get()
  passwordToEncode = password.get() 

  if len(userName) == 0 or len(passwordToEncode) == 0:
    message = 'Please fill in the inputs'
    loginError(message, loginWindow)

  passwordToEncode = passwordToEncode.encode("utf-8")
  password = base64.b64encode(passwordToEncode)
  cursor = conn.execute("SELECT * FROM appUsers Where userName = ?",[userName,]).fetchall()

  if len(cursor) == 0:
    message = 'Username does not exist'
    loginError(message, loginWindow)

  passwordToCheck = cursor[0][1]

  if password == passwordToCheck:
    print("Authorised")
    firstName = cursor[0][2]
    lastName = cursor[0][3]
    email = cursor[0][4]
    adminPrivalges = cursor[0][5]
    now = datetime.now()
    loginTime = now.strftime("%H:%M")

    if adminPrivalges == 1:
      adminPrivalges = True
      loginWindow.destroy()
      main(userName, firstName, lastName, email, adminPrivalges, loginTime)

    else:
      adminPrivalges = False
      loginWindow.destroy()
      main(userName, firstName, lastName, email, adminPrivalges, loginTime)

  else:
    message = 'Password incorrect please try again'
    loginError(message, loginWindow)
    print("Unauthorised")

def closePopUp(loginWindow, popUp):
  popUp.destroy()
  loginWindow.destroy()
  loginMenu()

def loginError(message, loginWindow):
  popUp = Tk()
  popUp.geometry('250x100')
  popUp.title('Alert!')
  label = Label(popUp, text=message, font=normFont)
  label.pack(side="top", fill="x", pady=10)
  button = Button(popUp, text="Okay", command = lambda: [closePopUp(loginWindow, popUp)])
  button.pack()
  popUp.mainloop()

def main(userName, firstName, lastName, email, adminPrivalges, loginTime):
  print("Username: ", userName)
  print("First name: ", firstName)
  print("Last name: ", lastName)
  print("Email: ", email)
  print("Admin privaleges: ", adminPrivalges)
  print("Login time: ", loginTime)

loginMenu()