# Importing requiered modules
import time
import sqlite3
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from mfrc522 import SimpleMFRC522
from picamera.array import PiRGBArray

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
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

def y():
    print("Y")
    time.sleep(3)
    camera.stop_recording()
    camera.stop_preview()

def n():
    print("N")
    time.sleep(3)
    camera.stop_recording()
    camera.stop_preview()
    
def main():
    recordingPath = ("/home/pi/Project/")
    videoFileName = "test"
    recordingTitle = (recordingPath + videoFileName + ".h264")
    camera.start_preview(alpha=200)
    time.sleep(0.25)
    camera.start_recording(recordingTitle)
    x = input("?: ")
    if x == "Y":
        y()
    if x == "N":
        n()

main()
