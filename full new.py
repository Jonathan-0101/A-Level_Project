import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys
import datetime
import sqlite3

conn = sqlite3.connect('System.db', check_same_thread=False)
conn.execute('''CREATE TABLE if not exists ENTRY_LOG
  (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  Authorised BOOLEAN NOT NULL,
  USER_ID TEXT NOT NULL,
  DateTime DATETIME NOT NULL);''')
conn.commit()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 14
reader = SimpleMFRC522()
GPIO.setup(PIR_PIN, GPIO.IN) # Setup GPIO pin PIR as input
print('Sensor initializing . . .')
time.sleep(15) # Give sensor time to start-up, 16 seconds
print('Active')
Relay_PIN = 4
GPIO.setup(Relay_PIN, GPIO.OUT)
GPIO.output(Relay_PIN, GPIO.LOW)

def lock():
    Relay_PIN = 4
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print('Door locked')
    time.sleep(5)

def unlock():
    Relay_PIN = 4
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print('Door unclocked')
    time.sleep(5)
    lock()
    
def pir(pin):
    print('Motion Detected!')
    print("Hold a tag near the reader")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))
    print()
    cursor=conn.execute("SELECT text FROM ID_CARDS Where ID = ?", [id]).fetchall()
    print(cursor)
    to_check = cursor[0]
    if to_check[0] == text:
        print('Authorised')
        Authorised = True
        Date_time = datetime.now()
        conn.execute("INSERT INTO ENTRY_LOG(Authorised, USER_ID, DateTime) VALUES (?,?,?)", [Authorised, id, Date_time]).lastrowid
        conn.commit()

        unlock()    
    else:
        print("not authorised")

GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100)
print('[Press Ctrl + C to end program!]')
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('\nScript ended')
finally:
    GPIO.cleanup()

