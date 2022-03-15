import time
import sqlite3
import RPi.GPIO as GPIO

Relay_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

conn = sqlite3.connect("System.db", check_same_thread=False)
conn.commit()


def main():
    #Creates while loop to check if there is an update to the db
    while True:
        cursor = conn.execute("SELECT * FROM doorStatus").fetchall()
        if cursor[0][0] == 1:
            #Calls unlock function and then locking function
            unlock()
            lock()
            time.sleep(5)
        else:
            time.sleep(5)

def unlock():
    #Unlocking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print("Door unlocked")
    #Timeout to give time for user to enter
    time.sleep(30)

def lock():
    #Relocking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print("Door locked")
    #Resseting value in db so that door can be unlocked again
    conn.execute("Update doorStatus set lockStatus = 0")
    conn.commit()


main()
