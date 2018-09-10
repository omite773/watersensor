import os
import time
import math
import subprocess
import sys
from time import sleep
from datetime import datetime
#Functions for sensor devices
import water_pump
import i2c_devices
import i2c_bb_devices

#Initiate availabilities for plugNplay functionality
arduinoAvailable = False
temperatureAvailable = False
#Keep sensor values global for ease of access
temperature = None
#sun = None
eleCond = None
battery = None
current = None

arduino_Vref = 5.0

local_const_timer = 100
usb_const_timer= 10
pump_const_timer = 200

usb_timer = usb_const_timer
local_timer = local_const_timer
pump_timer = pump_const_timer

#Figure out available devices at launch, also set certain settings
def initiate():
    if(i2c_devices.temp_init()):
        global temperatureAvailable
        temperatureAvailable = True

    if(i2c_bb_devices.arduino_init()):
        global arduinoAvailable
        arduinoAvailable = True

########## Function which handles storing values onto the .csv file #########    
#Write current measurement values to the log file
def append_log():
    if os.path.isdir("/home/pi/watersensor/data_logs/"):       
        try:
            #Open log file
            file = open("/home/pi/watersensor/data_logs/data_log.csv", "a")
        except IOError as e:
            #Some error logging
            print("IO-Err logger")
            log_error(str(e) + " Opening data_log.csv ERR")
            return 2

        if os.stat("/home/pi/watersensor/data_logs/data_log.csv").st_size == 0:
            #If log file empty, fill out header
            file.write('Time, Temp[C], EleCond [?], Battery[V], Current[mA]\n')
        #Then the sensor values separated by commas (.csv-format)
        file.write(datetime.now().strftime('%Y-%m-%d_%H:%M') + ", " + str(temperature) + ", " + str(eleCond) + ", " + str(battery) + ", " + str(current) + ", " + "\n" )
        file.close()
    else:
        #Error tracking
        print("Log dir not present")
        log_error("Log directory not found")


########## Functions which updates sensor values and logs data to .csv file and USB ##########
def update_sensors(Log, Backup):
    #Specify globals
    global arduinoAvailable
    global temperatureAvailable
    global temperature
    global eleCond
    global battery
    global current


    if(arduinoAvailable):
        try:
            (eleCond, battery, current) = i2c_bb_devices.read_arduino()
#            if(battery < 690 and battery > 0):
#                #Battery too low, arduino about to cut power
#                shutdown()
            #Convert from raw values to voltage
            print(eleCond)
            print(battery)
            eleCond = round(float(eleCond*arduino_Vref/1023),3) #What unit tho?
            battery = round(float(battery*arduino_Vref/1023),3) #V
            current = round(float(current*arduino_Vref*1000/(1023*4.74)),3) #mA
            #Calculate power drawn from solar panel to charge battery
            print("jahopp")
        except Exception as e:
            print("amenvadnuda")
            #Catch error and set arduino as unavailable in case of hardware failure
            arduinoAvailable = False
            eleCond = None
            battery = None
            current = None
            log_error(str(e) + " ARDUINO ERR, disabling")

    if(temperatureAvailable):
        try:
            temperature = i2c_devices.get_temperature()
        except Exception as e:
            #Catch sensor error and disable it
            temperature = None
            temperatureAvailable = False
            log_error(str(e) +  " TEMP_SENS ERR, disabling")

    append_log()
    if Log == True:
        #Log to local .csv file
        append_log()

#Copy "data_logs" file to a USB-stick 
#    if Backup == True:
#        #Backup all logs + picture to USB
#        #Run pic + copy scripts, return errors
#        err += subprocess.call(['sudo', 'sh', '/home/pi/watersensor/cp_to_usb.sh'])
#        if err != 0:
#            log_error(str(err) + " USB_mem or camera error")


#Simple shutdown function if battery is low
#def shutdown():
#    #Shutdown procedure, closes buses and syncs OS to SD-card
#    print("exiting")
#    log_error("Shutting down due to low battery")
#    i2c_bb_devices.close_bus()
#    i2c_devices.close_bus()
#    spi_devices.close_bus()
#    subprocess.call(['sudo', 'sync'])
#    subprocess.call(['sudo', 'shutdown', '-h', 'now'])
#    sys.exit()

def log_error(e):
    #Error logging
    file = open("/home/pi/watersensor/data_logs/error.txt", "a")
    file.write(datetime.now().strftime('%Y-%m-%d_%H:%M') + " Msg: " + e + "\n")
    file.close()

initiate()

########## Code which keeps code running and orginizes everything ##########
while(1):
    #Pumps water every ? seconds. 
    if pump_timer == 0:
        water_pump.water_pump(20)
        pump_timer = pump_const_timer
    else:
        pump_timer -= 1 #Counts down pump_timer 
        
        #Store values locally every ? seconds, and on USB ? seconds.
        local_timer -= 4
        if local_timer == 0:
            update_sensors(True, False)    #Remove this when project is done and up and running!
            local_timer = local_const_timer
#           if usb_timer == 0:
#                update_sensors(True, True) #log USB
#               usb_timer = usb_const_timer
#           else:
#                usb_timer -= 1
#               update_sensors(True, False) #log local
        else:
            update_sensors(False, False)
    sleep(0.8)
