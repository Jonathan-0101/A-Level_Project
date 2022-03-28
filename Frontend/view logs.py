#Importing required modules
import sqlite3

#Connecting to the database
conn = sqlite3.connect('database.db', check_same_thread = False)

print('\n'*10)

entryLogList = []

#Retriving information from the database
entryLog = conn.execute("SELECT * FROM entryLog").fetchall()

#For loop to populate the data list
for event in entryLog:
    eventId = event[0]
    entry = event[1]
    if entry == 1:
        entry = "Entry"
        userId = event[2]
        userDetails = conn.execute("SELECT firstName, lastName FROM idCards WHERE id = ?", (userId)).fetchall()
        firstName = userDetails[0][0]
        lastName = userDetails[0][1]
    else:
        userId = None
        entry = "No entry"
        firstName = None
        lastName = None
    dateTime = event[3]
    logInfo = [eventId, entry, userId, firstName, lastName, dateTime]
    entryLogList.append(logInfo)
for logItem in entryLogList:
    print(logItem)

print('\n'*10)
