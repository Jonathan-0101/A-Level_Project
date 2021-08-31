#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import sys
import datetime

GPIO.setwarnings(False)



reader = SimpleMFRC522()

while True:
    x=input("Do you want to read or write, R for read, W for write: ")
    if x == 'w':
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
        print()
    elif x == 'r':
        print("Hold a tag near the reader")
        reading = reader.read()
        print(reading)
        #print("ID: %s\nText: %s" % (id,text))
        print()
        datetime.datetime.now()
        f = open("Entry_Log.txt", "a+")
        x=str(datetime.datetime.now())
        f.write(x)
        f.write('\n')
        f.write(text)
        f.write('\n')
        f.write("entered")
        f.write('\n')
        f.close()
