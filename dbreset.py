import sqlite3

conn = sqlite3.connect('System.db', check_same_thread=False)
conn.execute("Update doorStatus set lockStatus = 0")
conn.commit()