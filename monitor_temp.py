import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import msvcrt


class Scope(object):
    def __init__(self, ax, maxt=2000, dt=1):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(15, 100)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter():
    'return a random value with probability p, else 0'

    while True:
 #       ser=serial.Serial('COM4')
        byte=ser.readline() #popraw na 6 jakby źle działało
        byte1=byte[:5]
        byte2=byte[-7:-2]
        string1=byte1.decode(encoding='UTF-8')
        string2=byte2.decode(encoding='UTF-8')
        print(string1, string2)
        yield float(string1)
        yield float(string2)
        time.sleep(1)
        if msvcrt.kbhit():
            break

ser=serial.Serial('COM5')
fig, ax = plt.subplots()
scope = Scope(ax)
 #pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,
                             blit=True)

plt.grid(True)
plt.show()
