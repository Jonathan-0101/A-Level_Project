import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute("Update doorStatus set lockStatus = 0")
conn.commit()
