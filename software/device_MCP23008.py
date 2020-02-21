import smbus
import time

class Device_MCP23008(): 

    registers = {
                    "IODIR"   : 0x00, # I/O Direction
                    "IOPOL"   : 0x01, # Input Polarity
                    "GPINTEN" : 0x02, # IOC Control
                    "DEFVAL"  : 0x03, # IOC Default Compare
                    "INTCON"  : 0x04, # Interrupt Control
                    "IOCON"   : 0x05, # Configuration
                    "GPPU"    : 0x06, # Pull-up Control
                    "INTF"    : 0x07, # Interrupt Flags
                    "INTCAP"  : 0x08, # Interrupt Capture
                    "GPIO"    : 0x09, # Port Register
                    "OLAT"    : 0x0A, # Output Latch
                }

    def __init__(self,Bus,address):
        self.Bus = Bus
        self.i2c_address = address
        return

    def read_pins(self):
        """
        Reads state of all 8x pins and returns byte
        """
        data = self.read_byte(self.registers["GPIO"])
        return data

    def write_pins(self,outputs):
        """
        Writes to outputs with single byte if set to output
        """
        self.write_byte(self.registers["GPIO"],outputs)
        return

    def write_directions(self,direction):
        """
        Sets I/O directions with single byte
        """
        self.write_byte(self.registers["IODIR"],direction)
        return

    def read_directions(self):
        """
        Reads state of I/O directions and returns byte
        """
        data = self.read_byte(self.registers["IODIR"])

    def write_byte(self,address,data):
        """
        Writes a single byte to an address
        """
        self.Bus.write_byte_data(self.i2c_address,address,data)
        return True

    def read_byte(self,address):
        """
        Reads a single byte from an address
        """
        data = self.Bus.read_byte_data(self.i2c_address,address)
        return data




if __name__ == "__main__":
    i2c_address = 0x20
    Bus = smbus.SMBus(1)

    IO_Expander = Device_MCP23008(Bus,i2c_address)

    IO_Expander.write_byte(0x00,0b11001111)
    IO_Expander.write_byte(0x09,0b11001111)

    print(IO_Expander.registers["GPIO"])

    print(IO_Expander.read_pins())
