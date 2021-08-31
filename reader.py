import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 14
reader = SimpleMFRC522()

card_info = reader.read()
f=open("temp.txt", "rt")
data = f.read()
data = data.replace('None', card_info)
f.close()
f = open("temp.txt", "wt")
f.write(data)
f.close()