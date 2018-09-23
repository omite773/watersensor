import pigpio
from time import sleep

temp_val_addr = 0x4f
temp_write_protect = 0x37

pi=pigpio.pi()
temp_handle = pi.i2c_open(1, temp_val_addr)
#arduino_handle = pi.i2c_open(1, 0x04)

#class I2CCommunicator:
       

class Arduino:
    def __init__(self, arduino_addr):
        self.addr = arduino_addr
        self.conn_handle = pi.i2c_open(1, self.addr)

    def send_temperature(self, raw_temperature):
        pi.i2c_write_i2c_block_data(self.conn_handle, 0x03, raw_temperature)

    def close(self):
        pi.i2c_close(self.conn_handle)

class Temperature:
    def __init__(self, temperature_addr):
        self.addr = temperature_addr
        self.conn_handle = pi.i2c_open(1, self.addr)
        # set 12 bit resolution, normal op mode, rest defaults 0b01100000
        self.send(0x01, 0x60)

    def get_temperature(self):
        self.send(0x01, 0x60)
        arr = self.receive(0x00, 2)
        #Sample arrives split, first part integer, last decimal
        temperature = int(arr[0]) + (int(arr[1] >> 4)*0.0625)
        #Compensate for two's-complement form
        #close_bus()
        if (int(arr[0]) & 0x80):
            temperature = 256 - temperature
        return (temperature, arr)

    def send(self, mode, data):
        pi.i2c_write_byte_data(self.conn_handle, mode, data)

    def receive(self, mode, count=1):
        pi.i2c_write_byte(self.conn_handle, mode)
        (cnt,bytearr) = pi.i2c_read_device(self.conn_handle, count)
        return bytearr

    def close(self):
        pi.i2c_close(self.conn_handle)


