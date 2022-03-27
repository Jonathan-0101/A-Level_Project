import os
import time
import sqlite3
import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime
from mfrc522 import SimpleMFRC522

videoFileName = 1

#Getting path to the file as will differ per computer
path = os.getcwd()
#Add the requiered video to the end of the path
fileName = (path + "\\Recordings\\" + videoFileName + ".h264")
camera = PiCamera() # Setting the camera that will be used
camera.resolution = (1920, 1080)
camera.framerate = 32 # Sets the frame rate of the camera
camera.start_preview(alpha=200)
time.sleep(0.1) # Delay for camera preview to start up
camera.start_recording(fileName) # Starts the recording