# Importing requiered modules
import time
import sqlite3
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from mfrc522 import SimpleMFRC522


conn = sqlite3.connect('System.db', check_same_thread=False) # Connects to the Database
conn.execute('''CREATE TABLE if not exists idCards 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  hashedId INTEGER,
  cardName VARCHAR,
  firstName TEXT,
  lastName TEXT,
  timeCreated DATETIME);''')
conn.execute('''CREATE TABLE if not exists entryLog 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  authorised INTEGER,
  userId INTEGER,
  dateTime DATETIME)''') # Creates the tables if it does not exist
conn.commit() # Commits to the database

# Seting up the Pins and devices connected to the Rasberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIR_PIN = 14
reader = SimpleMFRC522()

GPIO.setup(PIR_PIN, GPIO.IN) # Setup GPIO pin PIR as input
print('Sensor initializing . . .')
time.sleep(15) # Give sensor time to start-up, 16 seconds
print('Active')

Relay_PIN = 4


def cameraStop():
    time.sleep(10)
    global fileName
    global camera
    camera.stop_recording()
    camera.close()
    

def lock(): # Function for locking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print('Door locked')
    cameraStop()


def unlock(): # Function for unlocking the door and stopping the recording
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print('Door unclocked')
    lock()


def pir(pin): # Function for running the events when motion is detected
    now = datetime.now()
    dateTime = now
    cursor = conn.execute("SELECT * FROM entryLog").fetchall()
    
    if len(cursor) == 0:
        videoFileName = "1"
        
    else:    
        videoFileName = str(len(cursor))
        
    
    recordingPath = ("/home/pi/Project/Recordings/")
    global fileName
    fileName = (recordingPath + videoFileName + ".h264")
    global camera
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.framerate = 32
    camera.start_preview(alpha=200)
    time.sleep(0.1)
    camera.start_recording(fileName)
    print('Motion Detected!')
    cardId, cardName = reader.read()    # Reading the card
    cardId = cardId % 1999  # Hashing the cardId
    print()
    # Checks if the card is authorised
    cursor = conn.execute("SELECT text FROM idCards Where hashedId = ? and cardName = ?", [cardId, cardName]).fetchall()
    print(cursor)
    cardCheck = cursor[0]
    
    if len(cardCheck) == 1:
        print('Authorised')
        authorised = True
        # Adds the event into the entry log
        conn.execute("INSERT INTO entryLog(authorised, userId, dateTime) VALUES (?,?,?)", [authorised, cardId, dateTime])
        conn.commit()
        unlock() # Calls the function to unlock the door
    
    else:
        print("not authorised")
        time.sleep(15)
        authorised = False
        camera.stop_recording()
        camera.stop_preview()
        # Adds the event to the events log
        conn.execute("INSERT INTO entryLog(authorised, dateTime) VALUES (?,?)", [authorised, dateTime])
        conn.commit()

lock() # Calling the lock function on statrup to insure that teh door is locked

GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100) # Checks for motion


try:
    while True: # Loops the check for motion
        time.sleep(0.001)

    
except KeyboardInterrupt:
    print("\nScript ended")


finally:
    GPIO.cleanup()
