import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime
import mysql.connector
import numpy as np

# Prihlaseni do predem vytvorene databaze s nazvem "Senzor" a tabulkou: CREATE TABLE data (Datum DATETIME, Teplota DECIMAL(5,1), NadmorskaVyska DECIMAL(5,1), TlakVzduchu DECIMAL(5,1));
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database="Senzor",
)


fig = plt.figure()
rect = fig.patch
plt.style.use('ggplot')

mycursor = mydb.cursor()
  
# Fecthing Data From mysql to my python progame
mycursor.execute("SELECT Datum, Teplota, NadmorskaVyska, TlakVzduchu FROM data")
result = mycursor.fetchall

Datum = []
Teplota = []
NadmorskaVyska = []
TlakVzduchu = []

for i in mycursor:
    Datum.append(i[0])
    Teplota.append(i[1])
    NadmorskaVyska.append(i[2])
    TlakVzduchu.append(i[3])


# Visulizing Data using Matplotlib

ax1 = fig.add_subplot(212)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
ax1.clear()
ax1.plot(Datum,Teplota, "-g")
plt.title("Teplota")
        
ax2 = fig.add_subplot(221)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
ax2.clear()
ax2.plot(Datum,NadmorskaVyska)
plt.title("Nadmorska vyska")
        
ax3 = fig.add_subplot(222)
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
ax3.clear()
ax3.plot(Datum,TlakVzduchu)
plt.title("Tlak vzduchu")

plt.show()
