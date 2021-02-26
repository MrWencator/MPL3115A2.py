import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime

fig = plt.figure()
rect = fig.patch
rect.set_facecolor("#0079E7")
def animate(i):
    ftemp = "sensor.csv"
    fh = open(ftemp)
    temp = list()
    altitude = list()
    pressure = list()
    timeC = list()
    for line in fh:
        pieces = line.split(',')
        degree = pieces[1]
        nadmvyska = pieces[2]
        tlak = pieces[3]
        timeB = pieces[0]
            #print timeB
        time_string = datetime.strptime(timeB,"%d.%m. %H:%M:%S")
        #print time_string
        try:
            temp.append(float(degree))
            altitude.append(float(nadmvyska))
            pressure.append(float(tlak))
            timeC.append(time_string)
        except:
            print "neznam"
        

        ax1 = fig.add_subplot(212)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M:%S"))
        ax1.clear()
        ax1.plot(timeC,temp, "C", linewidth = 3.3)
        plt.title("Temperature")
        
        ax2 = fig.add_subplot(221)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M:%S"))
        ax2.clear()
        ax2.plot(timeC,altitude, "m", linewidth = 3.3)
        plt.title("Altitude")

        
        #ax3 = fig.add_subplot(222)
        #ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M:%S"))
        #ax3.clear()
        #ax3.plot(timeC,pressure, "kPa", linewidth = 3.3)
        #plt.title("Pressure")
        
ani = animation.FuncAnimation(fig, animate, interval = 6000)   
plt.show()
