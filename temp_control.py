#This function assumes that there is no loss of heat ever, period

from time import sleep
import RPi.GPIO as GPIO


PIN = 6 #Which pin on RPi that switches the heater on/off
target_temp = 20.0 #The temperature we want to get to
Ttemp = None

######## changes are done if chamber and heater is changed ########
water_const = 4.2 #constant for heating 1kg water 1C (kJ/kg/K) 
density_water = 997 #in kg/m^3 
chamber_volume = 0.008 #in m3
power_heater = 1 #power of heater in watt !!!!!!!CHANGE WHEN WE GET A ANSWER ON THIS!!!!!!!!

mass_water = density_water*chamber_volume #in kg


#simple temperature regulating function using the above constants temperature differance
def temp_regulation(temperature):
    print(temperature)
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)

        Ttemp =  target_temp - temperature
        time = round(water_const*mass_water*Ttemp/power_heater) #in seconds

        GPIO.output(PIN, GPIO.HIGH)
        sleep(time)
        GPIO.output(PIN, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()
        
##### TESTING HEATER #####            
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN,GPIO.OUT)

#GPIO.output(PIN, GPIO.HIGH)
#sleep(30)
#GPIO.output(PIN,GPIO.LOW)
