import pigpio
from time import sleep

temp_val_addr = 0x4f
temp_write_protect = 0x37

pi=pigpio.pi()
temp_val_bus = pi.i2c_open(1, temp_val_addr)


########## i2c functions ##########
def close_bus():
    pi.i2c_close(temp_val_bus)
#    pi.stop()


def send(bus, mode, data):
    pi.i2c_write_byte_data(bus, mode, data)


def recieve(bus, mode, count=1):
    pi.i2c_write_byte(bus, mode)
    (cnt,bytearr) = pi.i2c_read_device(bus,count)
    return bytearr


########## Temperature functions ##########
def temp_init():
    try:
        #set 12 bit resolution, normal op mode, rest defaults 0b01100000
        send(temp_val_bus, 0x01, 0x60)
        close_bus()
        return 1
    except pigpio.error:
        return 0


def get_temperature():
    pi.i2c_open(1, temp_val_addr)
    sleep(2)
    send(temp_val_bus, 0x01, 0x60)
    sleep(2)
    arr = recieve(temp_val_bus, 0x00, 2)
    #Sample arrives split, first part integer, last decimal
    temperature = int(arr[0]) + (int(arr[1] >> 4)*0.0625)
    #Compensate for two's-complement form
    close_bus()
    if (int(arr[0]) & 0x80):
        temperature = 256 - temperature
    return (temperature, arr)
