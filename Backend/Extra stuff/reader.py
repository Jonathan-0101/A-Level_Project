import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 14
reader = SimpleMFRC522()
card_info = str(reader.read(timeout = 15))
print(card_info)
f = open("temp.txt", "wt")
f.write(card_info)
f.close()
