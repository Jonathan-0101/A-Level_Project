import os
import mariadb
from dotenv import load_dotenv

load_dotenv()
dbIp = os.getenv("dbIp")
dbUserName = os.getenv('dbUserName')
dbPassword = os.getenv('dbPassword')

cur = mariadb.connect(host=dbIp,
                        database='iSpy',
                        user=dbUserName,
                        password=dbPassword)


conn = cur.cursor()

# info = cur.execute('SELECT dateTime FROM entryLog')
# print(info)


# get = cur.execute('SHOW TABLES')
# print(get)

'''
get all information from appUsers table
'''
info = conn.execute('SELECT * FROM entryLog')
info = conn.fetchall()  
time = (info[0][3])
print(time.strftime('%d-%m-%Y %H:%M:%S'))
