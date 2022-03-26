import time
import sqlite3
import RPi.GPIO as GPIO

Relay_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

conn = sqlite3.connect("System.db", check_same_thread=False)

def unlock():
    # Function for unlocking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.HIGH)
    print("Door unlocked")
    # Timeout to give user oppotunity to enter door
    time.sleep(30)

def lock():
    # Function for locking the door
    GPIO.setup(Relay_PIN, GPIO.OUT)
    GPIO.output(Relay_PIN, GPIO.LOW)
    print("Door locked")
    # Resseting value in db so that door can be unlocked again
    conn.execute("Update doorStatus set lockStatus = 0")
    conn.commit()

def main():
    # Creates while loop to check if there is an update to the database
    while True:
        # Retriveing the doorStatus value from the table
        cursor = conn.execute("SELECT * FROM door Status").fetchall()
        # Checks if the value is equal to 1 (whether it should open)
        if cursor[0][0] == 1:
            # Calls unlock function and then locking function
            unlock()
            lock()
            # Adds a time delay before the table is checked again
            time.sleep(5)
        else:
            # Adds a time delay before the table is checked again
            time.sleep(5)

lock() # Ensures door is locked when the program starts up
main()
