import smbus
import time

class Device_24LC16B(): 
    def __init__(self,Bus,address):
        self.Bus = Bus
        self.i2c_address = address
        return

    def write_byte(self,address,data):

        self.Bus.write_byte_data(self.i2c_address,address,data)

        return True

    def read_byte(self,address):
        data = self.Bus.read_byte_data(self.i2c_address,address)
        return data

if __name__ == "__main__":
    i2c_address = 0x50
    Bus = smbus.SMBus(1)

    EEPROM_bank0 = Device_24LC16B(Bus,i2c_address)
    EEPROM_bank1 = Device_24LC16B(Bus,i2c_address+1)

    while(1==1):

    #    for x in range(0,10):
    #        EEPROM_bank0.write_byte(x,x*2)
    #        time.sleep(0.01)
        for x in range(0,10):
            print(x,EEPROM_bank0.read_byte(x))
            time.sleep(0.01)

    #    for x in range(0,10):
    #        EEPROM_bank1.write_byte(x,x+1)
    #        time.sleep(0.01)
        for x in range(0,10):
            print(x,EEPROM_bank1.read_byte(x))
            time.sleep(0.01)

