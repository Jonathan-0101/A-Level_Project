import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
reader = SimpleMFRC522()
PIR_PIN = 14 # Assign GPIO4 pin 7 to PIR
GPIO.setup(PIR_PIN, GPIO.IN) # Setup GPIO pin PIR as input
print('Sensor initializing . . .')
time.sleep(15) # Give sensor time to start-up, 60 seconds
print('Active')
def pir():
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('Motion Detected!')
    print("Hold a tag near the reader")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))
    f = open("Entry_Log.txt", "a+")
    f.write(dt_string, "-", text)
    f.close()
    print()
    time.sleep(10)
GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100)
print('[Press Ctrl + C to end program!]')
while True:
    time.sleep(0.001)
    GPIO.cleanup()
