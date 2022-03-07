#Importing required modules
import sqlite3

#Connecting to the database
conn = sqlite3.connect('System.db', check_same_thread = False)

entryLogList = []

#Retriving information from the database
entryLog = conn.execute("SELECT * FROM entryLog").fetchall()

#For loop to populate the data list
for i in range(len(entryLog)):
    eventId = entryLog[i][0]
    entry = entryLog[i][1]
    if entry is 1:
        entry = "Entry"
        userId = entryLog[i][2]
        userDetails = conn.execute("SELECT firstName, lastName FROM idCards WHERE id = ?", (userId, )).fetchall()
        firstName = userDetails[0][0]
        lastName = userDetails[0][1]
    else:
        userId = None
        entry = "No entry"
        firstName = None
        lastName = None
    dateTime = entryLog[i][3]
    logInfo = [eventId, entry, userId, firstName, lastName, dateTime]
    entryLogList.append(logInfo)
for x in range(len(entryLogList)):
    print(entryLogList[x])
