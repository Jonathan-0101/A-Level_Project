import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from picamera import PiCamera
import time
from datetime import datetime
import sqlite3

camera = PiCamera()
conn = sqlite3.connect('System.db', check_same_thread=False)
conn.execute('''CREATE TABLE if not exists ENTRY_LOG
  (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  Authorised BOOLEAN NOT NULL,
  USER_ID TEXT NOT NULL,
  DateTime VARCHAR NOT NULL);''')
conn.commit()
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
    card_id, to_check = reader.read(timeout = 20)
    print()
    cursor=conn.execute("SELECT text FROM ID_CARDS Where ID = ?", [card_id]).fetchall()
    print(cursor)
    to_check = cursor[0]
    if to_check[0] == cursor:
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
print('[Press Ctrl + C to end program!]')
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('\nScript ended')
finally:
    GPIO.cleanup()

