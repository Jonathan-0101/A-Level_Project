import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Relay_PIN = 4
GPIO.setup(Relay_PIN, GPIO.OUT)
print('[press ctrl+c to end the script]')
try: # Main program loop
    while True:
        GPIO.output(Relay_PIN, GPIO.HIGH)
        print('Door unclocked')
        sleep(3) # Waitmode for 1 second
        GPIO.output(Relay_PIN, GPIO.LOW)
        print('Door locked')
        sleep(3) # Waitmode for 1 second
# Scavenging work after the end of the program
except KeyboardInterrupt:
    print('Script end!')
finally:
    GPIO.cleanup()