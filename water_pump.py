import datetime
import time
import RPi.GPIO as GPIO

#GPIO.setwarnings(False)

PIN = 12
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
