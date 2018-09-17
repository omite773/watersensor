import sys
from time import sleep
import subprocess

wifi_status = False

#Quick function which switches wifi on and sends data
def wifi_on():
    subprocess.call("sudo ifconfig wlan0 up", shell = True)
    wifi_status = True

def wifi_off():
    subprocess.call("sudo ifconfig wlan0 down", shell = True)
    wifi_status = False

