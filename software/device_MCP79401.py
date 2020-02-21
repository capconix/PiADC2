import smbus
import time
import datetime

class Device_MCP79401(): 
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

    def split_two_digit(self,value):
        value = value % 100
        tens = int(value / 10)
        ones = value % 10
        return tens,ones

    def is_leap_year(self,year):
        if(year % 400 == 0):
            return 1
        if(year % 100 == 0):
            return 0
        if(year % 4 == 0):
            return 1
        else:
            return 0

    def write_date_time(self,datetime_object):
        seconds = datetime_object.second
        seconds_tens,seconds_ones = self.split_two_digit(seconds)

        minutes = datetime_object.minute
        minutes_tens,minutes_ones = self.split_two_digit(minutes)

        hours = datetime_object.hour
        hours_tens,hours_ones = self.split_two_digit(hours)

        day = datetime_object.day
        day_tens,day_ones = self.split_two_digit(day)

        month = datetime_object.month
        month_tens,month_ones = self.split_two_digit(month)

        year = datetime_object.year
        year_tens,year_ones = self.split_two_digit(year)

        # TODO make day of week and leapyear set correctly
        dow = datetime_object.weekday()
        leap_year = self.is_leap_year(datetime_object.year)

        RTCSEC = seconds_ones + (seconds_tens << 4) + 0b10000000
        RTCMIN = minutes_ones + (minutes_tens << 4)
        RTCHOUR = hours_ones + (hours_tens << 4)
        RTCDATE = day_ones + (day_tens << 4)
        RTCMTH = (leap_year << 5) + month_ones + (month_tens << 4)
        RTCYEAR = year_ones + (year_tens << 4)


        print("year",year_tens,year_ones)
        print("month",month_tens,month_ones)
        print("day",day_tens,day_ones)
        print("hours",hours_tens,hours_ones)
        print("minutes",minutes_tens,minutes_ones)
        print("seconds",seconds_tens,seconds_ones)


        data = [RTCSEC,RTCMIN,RTCHOUR,0b00101000,RTCDATE,RTCMTH,RTCYEAR]

        self.Bus.write_i2c_block_data(self.i2c_address,0x00,data)

        return

    def read_date_time(self):
        data = self.Bus.read_i2c_block_data(self.i2c_address,0x00,7)

        datetime_data = []

        # Seconds
        temp = data[0]
        seconds_ones = temp & 0b00001111
        seconds_tens = ((temp & 0b01110000) >> 4) * 10
        seconds = seconds_ones + seconds_tens
        datetime_data.append(seconds)

        # Minutes
        temp = data[1]
        minutes_ones = temp & 0b00001111
        minutes_tens = ((temp & 0b01110000) >> 4) * 10
        minutes = minutes_ones + minutes_tens
        datetime_data.append(minutes)

        # Hours
        temp = data[2]
        hours_ones = temp & 0b0001111
        hours_tens = ((temp & 0b00110000) >> 4) * 10
        hours = hours_ones + hours_tens
        datetime_data.append(hours)

        # DOW
        temp = data[3]
        dow = temp & 0b00000111
        running = (temp & 0b00100000) >> 5
        power_fail = (temp & 0b00010000) >> 4
        vbatt = (temp & 0b00001000) >> 3
        datetime_data.append([dow,running,power_fail,vbatt])

        # Date
        temp = data[4]
        day_ones = temp & 0b00001111
        day_tens = ((temp & 0b00110000) >> 4) * 10
        day = day_ones + day_tens
        datetime_data.append(day)

        # Month
        temp = data[5]
        month_ones = temp & 0b00001111
        month_tens = ((temp & 0b00010000) >> 4) * 10
        month = month_ones + month_tens
        datetime_data.append(month)
        leap_year = (temp & 0b00100000) >> 5
        datetime_data.append(leap_year)

        # Year
        temp = data[6]
        year_ones = temp & 0b00001111
        year_tens = ((temp & 0b11110000) >> 4) * 10
        year = year_ones + year_tens
        datetime_data.append(year)

        print(datetime_data)

        # TODO turn into datetime object

        return data


if __name__ == "__main__":
    i2c_address = 0x6f
    Bus = smbus.SMBus(1)

    RTC = Device_MCP79401(Bus,i2c_address)

    datetime_object = datetime.datetime.now()

    #RTC.write_date_time(datetime_object)

    print(RTC.read_date_time())
