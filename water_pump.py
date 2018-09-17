import datetime
import time
import RPi.GPIO as GPIO

PIN = 12

def water_pump(forLength):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)

        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(forLength)

        GPIO.output(PIN, GPIO.LOW)
        time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
