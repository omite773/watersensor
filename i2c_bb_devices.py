import pigpio
import math
from time import sleep

arduino_addr = 0x04

SDA = 22
SCL = 27
pi = pigpio.pi()

#Close bus if already open
try:
    pi.bb_i2c_close(SDA)
    sleep(0.2)
except pigpio.error as e:
    print(str(e) + " Startar om bb i2c port " + str(SDA))

#Open bus on GPIO pins, 300KHz
bus = pi.bb_i2c_open(SDA,SCL,300000)

def close_bus():
    pi.bb_i2c_close(SDA)
    pi.stop()

def temp_send():
    #Bit-banging array
    (s, buf) = pi.bb_i2c_zip(SDA,[4, arduino_addr, 2, 7, 1, 0x03, 3, 0])

def recieve(addr,mode,count):
    #Specify register address
    (s, buf) = pi.bb_i2c_zip(SDA,[4, addr, 2, 7, 1, mode, 3, 0])
    #Read specified register
    (s, buf) = pi.bb_i2c_zip(SDA,[4, addr, 2, 6, count, 3, 0])
    if s >= 0:
        return buf
    else:
        #S should be positive if recieved correctly
        raise ValueError('i2c error returned s < 0 on recieve')


########## Functions for reading Arduino ##########
def arduino_init():
    try:
        #(tmp,tmp2,tmp3) = read_arduino()
        return 1
    except pigpio.error:
        #Arduino not connected
        return 0

def read_arduino():
    #temp = temp_send()
    #print "My temp: ", temp
    #Get energy values from arduino, indexes 0 and 1
    #Arrives on split form, lower byte first
    eleCondRaw = recieve(arduino_addr, 0x00, 2)
    eleCond = (int(eleCondRaw[1]) << 8) | int(eleCondRaw[0])
    battVRaw = recieve(arduino_addr, 0x01, 2)
    batteryV = (int(battVRaw[1]) << 8) | int(battVRaw[0])
    currentRaw = recieve(arduino_addr, 0x02, 2)
    current = (int(currentRaw[1]) << 8) | int(currentRaw[0])
    return (eleCond, batteryV, current)


#May not be used!
########## Setting environment via temperature sensor #########
def set_environment(temperature, humidity = 50 ):
    # Minimum enterable temperature
    if temperature < -25.0:
        temperature = -25.0
    # Check humidity bounds
    if humidity < 0 or humidity > 100.0:
        humidity = 50
    # LSB is worth 0.5C and so on
    hum_perc = int(round(humidity)) << 1
    # Split fractionals and integers
    parts = math.modf(temperature)
    # Remove sign bit from fractional part
    fractional = math.fabs(parts[0])
    temp_int = int(parts[1])
    # Add offset and shift 9
    temp_high = ((temp_int + 25) << 9)
    # LSB of fractional is worth 1/512, but must be sent as integer
    temp_low = (int(fractional / 0.001953125) & 0x1FF)
    # Merge result
    temp_conv = (temp_high | temp_low)
    # Complete bytearray with humidity
    buf = [hum_perc, 0x00,((temp_conv >> 8) & 0xFF), (temp_conv & 0xFF)]
