import os
import time
from picamera import PiCamera


videoFileName = "100"

#Getting path to the file as will differ per computer
path = os.getcwd()
#Add the requiered video to the end of the path
fileName = (path + "/Recordings/" + videoFileName + ".h264")
print(fileName)
camera = PiCamera() # Setting the camera that will be used
camera.close()
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 30 # Sets the frame rate of the camera
camera.start_preview(alpha=200)
time.sleep(0.1) # Delay for camera preview to start up
camera.start_recording(fileName) # Starts the recording
time.sleep(10)
camera.stop_recording()
camera.close()
