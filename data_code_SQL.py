import smbus
import csv
import time
from datetime import datetime
import mysql.connector

# Prihlaseni do predem vytvorene databaze s nazvem "Senzor" a tabulkou: CREATE TABLE data (Datum DATETIME, Teplota DECIMAL(5,1), NadmorskaVyska DECIMAL(5,1), TlakVzduchu DECIMAL(5,1));
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database="Senzor",
)

# Ziskani cursor metodou cursor()
cur = db.cursor()

# Nekonecny loop
while True:

# Nacitani hodnot ze senzoru
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

# Zaokrouhleni hodnot na jedno desetinne misto
    nadmorskaVyska = round(nadmorskaVyska, 1)
    teplota = round(teplota, 1)
    tlakVzduchu = round(tlakVzduchu, 1)
    now = datetime.now()
    cas = now.strftime("%Y-%m-%d %H:%M:%S")

# INSERT hodnot do databaze
    ulozeni_hodnot = "INSERT INTO data (Datum, Teplota, NadmorskaVyska, TlakVzduchu) VALUES ('%s', %s, %s, %s)" % (cas, teplota, nadmorskaVyska, tlakVzduchu)
    cur.execute(ulozeni_hodnot)
    
# To ensure the Data Insertion, commit database
    db.commit()
    print(cur.rowcount, "data byla uspesne zapsana")
    
# Nastaveni za jak dlouho se ma provadet mereni
    time.sleep(10)

# Ukonceni spojeni s databazi
db.close()
