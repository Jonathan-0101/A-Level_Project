import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Hold a tag near the reader")

try:
    id, text = reader.read(timeout=5)
    if id == None:
        print("Timedout before card was read")
    else: 
        print(id)
        print(text)

finally:
    GPIO.cleanup()
