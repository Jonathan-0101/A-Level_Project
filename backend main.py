# Importing requiered modules
import os
import time
import mariadb
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522

load_dotenv()
dbIp = os.getenv("dbIp")
dbUserName = os.getenv('dbUserName')
dbPassword = os.getenv('dbPassword')

cur = mariadb.connect(host=dbIp, database='iSpy', user=dbUserName, password=dbPassword)

conn = cur.cursor()

# Seting up the Pins and devices connected to the Rasberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 14
reader = SimpleMFRC522()
GPIO.setup(PIR_PIN, GPIO.IN)  # Setup GPIO pin PIR as input
print('Sensor initializing . . .')
time.sleep(15)  # Give sensor time to start-up, 15 seconds
print('Active')
Relay_PIN = 4


def cameraStop(fileName, camera):
    time.sleep(10)
    camera.stop_recording()
    camera.close()


def lock():  # Function for locking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print('Door locked')


def unlock():  # Function for unlocking the door and stopping the recording
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print('Door unlocked')
    time.sleep(30)


def lockMain(fileName, camera):  # Function for locking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print('Door locked')
    cameraStop(fileName, camera)


def unlockMain(fileName, camera):  # Function for unlocking the door and stopping the recording
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    time.sleep(10)
    print('Door unlocked')
    lockMain(fileName, camera)


def pir(pin):  # Function for running the events when motion is detected
    now = datetime.now()  # Getting current date and time
    dateTime = now
    cursor = conn.execute("SELECT * FROM entryLog")
    cursor = conn.fetchall()

    # Naming the video file in relation to the event id
    if len(cursor) == 0:
        videoFileName = "1"

    else:
        videoFileName = str(len(cursor)+1)

    # Getting path to the file as will differ per computer
    path = os.getcwd()
    # Add the requiered video to the end of the path
    fileName = (path + "/Recordings/" + videoFileName + ".h264")
    camera = PiCamera()  # Setting the camera that will be used
    camera.resolution = (1920, 1080)
    camera.framerate = 25  # Sets the frame rate of the camera
    camera.start_preview(alpha=200)
    time.sleep(0.1)  # Delay for camera preview to start up
    camera.start_recording(fileName)  # Starts the recording
    print('Motion Detected!')
    # Setting default values for cardId and cardName if they do not get written
    cardId = None
    cardName = None
    cardId, cardName = reader.read(timeout=20)  # Reading the card waiting for 20 seconds if no card is scanned
    cardId = cardId  # Hashing the cardId

    # Checks if the card is authorised
    cursor = conn.execute("SELECT text FROM idCards Where cardId = ? and cardName = ? and active = 1", (cardId, cardName,))
    cursor = conn.fetchall()
    cardCheck = cursor[0]

    if len(cardCheck) == 1:
        print('Authorised')
        authorised = True
        # Adds the event into the entry log
        conn.execute("INSERT INTO entryLog(authorised, userId, dateTime) VALUES (?,?,?)", (authorised, cardId, dateTime,))
        cur.commit()
        unlock(fileName, camera)  # Calls the function to unlock the door

    else:
        print("Not authorised")
        time.sleep(15)
        authorised = False
        camera.stop_recording()
        camera.stop_preview()
        # Adds the event to the events log
        conn.execute("INSERT INTO entryLog(authorised, dateTime) VALUES (?,?)", (authorised, dateTime,))
        cur.commit()


lock()  # Calling the lock function on statrup to lock the door incase there is a power loss
camera = PiCamera()
camera.close()

GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100)  # Checks for motion

try:
    while True:  # Loops the check for motion
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nScript ended")

finally:
    GPIO.cleanup()
