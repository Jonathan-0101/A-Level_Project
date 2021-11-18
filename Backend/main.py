import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from picamera import PiCamera
import time
from datetime import datetime
import sqlite3

camera = PiCamera() #Sets up the camera for use later on
conn = sqlite3.connect('System.db', check_same_thread=False) #Connects to the DataBase
conn.execute('''CREATE TABLE if not exists ID_CARDS 
  (ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  Hashed_ID INTEGER NOT NULL,
  text VARCHAR NOT NULL,
  First_name TEXT NOT NULL,
  Last_name TEXT NOT NULL,
  Time_created DATETIME NOT NULL);''') #Creates the DataBase if it does not exist
conn.commit() #Commits to the database
#Seting up the Pins and devices connected to the Rasberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 14
reader = SimpleMFRC522()
GPIO.setup(PIR_PIN, GPIO.IN) # Setup GPIO pin PIR as input
print('Sensor initializing . . .')
time.sleep(15) # Give sensor time to start-up, 15 seconds
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
    time.sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    lock()
    
def pir(pin):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y %H¦%¦%S")
    recording_path = ("/home/pi/Documents/Project/Recordings/")
    recording_title = (recording_path + dt_string + ".h264")
    camera.start_preview()
    camera.start_recording(recording_title)
    print('Motion Detected!')
    print("Hold a tag near the reader")
    #Reading card and waiting with timeout
    card_id, username = reader.read(timeout = 20)
    card_id = card_id % 1999
    print()
    cursor=conn.execute("SELECT text FROM ID_CARDS Where Hashed_ID = ? and Username = ?", [card_id, username]).fetchall()
    print(cursor)
    to_check = cursor[0]
    if len(to_check) == 1:
        print('Authorised')
        Authorised = True
        conn.execute("INSERT INTO ENTRY_LOG(Authorised, USER_ID, DateTime) VALUES (?,?,?)", [Authorised, card_id, dt_string]).lastrowid
        conn.commit()
        unlock()    
    else:
        print("not authorised")
        time.sleep(15)
        Authorised = False
        camera.stop_recording()
        camera.stop_preview()
        conn.execute("INSERT INTO ENTRY_LOG(Authorised, DateTime) VALUES (?,?,?)", [Authorised, dt_string]).lastrowid
        conn.commit()

GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100)
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('\nScript ended')
finally:
    GPIO.cleanup()