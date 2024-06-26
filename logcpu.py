## This code grew out of a raspberrypi.org "temperature log" project. For now, I have commented out the
## graphing functionality and expanded the data being logged to include cpu volts and frequencies.
## This was written for a rasberry pi 3B+ running Raspbian 11 Bullseye.

import subprocess
import os
from gpiozero import CPUTemperature
from time import sleep, strftime, time
#import matplotlib.pyplot as plt    #for plotting


## Enable for graphing functionality
#plt.ion()
#x = []
#y = []


cpu = CPUTemperature()


## 0:time, 1:temp, 2-5:core frequencies, 6:fahreneheit, 7: scaling governor, 8: used memory MBs
def write_temp(temp,cpu0freq,cpu1freq,cpu2freq,cpu3freq,ftemp,gov,memused,throttled):
    with open("./cpustats.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temp), 
            ##str(volts[1][5:]), 
            str(cpu0freq), str(cpu1freq), str(cpu2freq), str(cpu3freq),str(ftemp),str(gov),str(memused),str(throttled)))

        

## Enable for graphing functionality.
#def graph(temp):
#    y.append(temp)
#    x.append(time())
#    plt.clf()
#    plt.scatter()
#    plt.plot(x,y)
#    plt.draw()


## Loop that populates the variables and calls the writing proc. Change sleep() to preferred # of seconds between log entries.
while True:
    temp = cpu.temperature
    ##volts = (subprocess.getstatusoutput('vcgencmd measure_volts'))
    cpu0freq = os.popen('cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq').read().strip()
    cpu1freq = os.popen('cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq').read().strip()
    cpu2freq = os.popen('cat /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq').read().strip()
    cpu3freq = os.popen('cat /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq').read().strip()
    ftemp = round((((temp) * 9 / 5 ) + 32),2)
    gov = os.popen('cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor').read().strip()
    memused = round(int(os.popen('cat /proc/meminfo | grep Active: | tr -d -c 0-9').read().strip())/1000,2)
    throttled = (subprocess.getstatusoutput('vcgencmd measure_volts'))
    write_temp(temp,cpu0freq,cpu1freq,cpu2freq,cpu3freq,ftemp,gov,memused,throttled)
    print("Day+Time:    " + strftime("%Y-%m-%d %H:%M:%S"))
    print("Temp(C):     " + str(temp))
    print("Temp(F):     " + str(ftemp))
    ##print("Volts:       " + str(volts[1][5:]))
    print("cpu0freq:    " + str(cpu0freq))
    print("cpu1freq:    " + str(cpu1freq))
    print("cpu2freq:    " + str(cpu2freq))
    print("cpu3freq:    " + str(cpu3freq))
    print("Scaling Gov: " + str(gov))
    print("Used Memory: " + str(memused))
    print("Throttled:   " + str(throttled))
    sleep(10)
#   graph(temp)
#   plt.pause(10)
