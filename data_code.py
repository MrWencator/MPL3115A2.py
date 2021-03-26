import smbus
import csv
import time
import datetime


with open("sensor.csv", "a") as csvsoubor:
    while True:

        bus = smbus.SMBus(1)

        bus.write_byte_data(0x60, 0x26, 0xB9)
        bus.write_byte_data(0x60, 0x13, 0x07)
        bus.write_byte_data(0x60, 0x26, 0xB9)

        time.sleep(1)

        data = bus.read_i2c_block_data(0x60, 0x00, 6)

        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        nadmorskaVyska = tHeight / 16.0
        teplota = temp / 16.0

        bus.write_byte_data(0x60, 0x26, 0x39)

        time.sleep(1)

        data = bus.read_i2c_block_data(0x60, 0x00, 4)

        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        tlakVzduchu = (pres / 4.0) / 1000.0

        nadmorskaVyska = round(nadmorskaVyska, 1)
        teplota = round(teplota, 1)
        tlakVzduchu = round(tlakVzduchu, 1)
        
        cas = time.strftime("%d")+"."+time.strftime("%m")+". " +time.strftime("%H")+":"+time.strftime("%M")
        hodnoty = [cas, teplota, nadmorskaVyska, tlakVzduchu]
        print("cas: {0} Teplota: {1} Nadmorska vyska: {2} Tlak vzduchu: {3}".format(cas, teplota, nadmorskaVyska, tlakVzduchu))
        sensorwriter = csv.writer(csvsoubor)
        sensorwriter.writerow(hodnoty)
        time.sleep(5)

