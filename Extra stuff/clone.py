#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import sys

GPIO.setwarnings(False)
reader = SimpleMFRC522()
input()
id, text = reader.read()
print("card scanned, switch tag")
f = open("to_use.txt", "a")
id1 = str(id)
print(id1)
print(text)
x = [id1, text]
str1 = ""
for i in x:
    str1 = str1 + x[i]
f.write(str1)
f.close()
print("5")
time.sleep(1)
print("4")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
reader.write(text)
print("Done")
