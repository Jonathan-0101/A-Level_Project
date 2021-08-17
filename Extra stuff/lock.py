import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
def lock():
    Relay_PIN = 4
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print('Door locked')
    menu()

def unlock():
    Relay_PIN = 4
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print('Door unclocked')
    menu()

def menu():
    x=input("Lock or unlock? ")
    if x == 'l':
        lock()
    if x == 'u':
        unlock()
    else:
        print("Error")
        print("Try again")
        menu()
menu()
