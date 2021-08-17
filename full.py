import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys
import datetime
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

def unlock():
    Relay_PIN = 4
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print('Door unclocked')
    
def pir(pin):
    print('Motion Detected!')
    print("Hold a tag near the reader")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))
    print()
    id1 = str(id)
    for z in range(len(text)):
        text.replace(" ", "")
    print(text)
    to_check = (id1+text)
    for y in range(len(to_check)):
        to_check.replace(" ", "")
    print(to_check)
    datetime.datetime.now()
    f = open("Users.txt", "r")
    authorised = f.readlines()
    for i in range(len(authorised)):
        line_text = authorised[i]
        line_text.replace(" ", "")
        print(line_text)
        if to_check ==  line_text:
            unlock()
            print("Authorised")
            time.sleep(5)
            lock()
    else:
        print("not authorised")
    #x=str(datetime.datetime.now())
    #to_w = str(x, text, "entered")
    #f.write(text)
    #f.write('\n')
    #f.close()
GPIO.add_event_detect(14, GPIO.FALLING, callback=pir, bouncetime=100)
print('[Press Ctrl + C to end program!]')
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('\nScript ended')
finally:
    GPIO.cleanup()
