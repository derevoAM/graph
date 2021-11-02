import RPi.GPIO as g
import time
import matplotlib.pyplot as plt
import numpy as np

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24] 
mas = []
vol = []

def dec2bin(a):
    return [int(i) for i in bin(a)[2:].zfill(8)]
def bin2dac(a):
    signal = dec2bin(a)
    g.output(dac, signal)
    g.output(leds, signal)
    return signal

troykaModule = 17

g.setmode(g.BCM)
g.setup(dac, g.OUT, initial = g.LOW)
g.setup(leds, g.OUT, initial = g.LOW)
g.setup(troykaModule, g.OUT, initial  = g.HIGH)
g.setup(4, g.IN)



def adc():
    b = 0
    n = 0 #количество измерений
    while b < 250:
        ar = [0, 0, 0, 0, 0, 0, 0, 0]
        b = 0
        c = 0
        for i in range(8):
            c += 2**(7 - i)
            signal = bin2dac(c)
            time.sleep(0.001)
            compvalue = g.input(4)
            if compvalue == 0:
                ar[i] = 0
                c -= 2**(7 - i)
            else:
                ar[i] = 1
                b += 2**(7 - i)
        V = (b / 256) * 3.3
        vol.append(V)
        print("Digital Value : {}, input voltage = {:.2f}".format(b, V))
        mas.append(b)
        n += 1
        #print(ar)
    g.output(troykaModule, 0)
    while b > 5:
        ar = [0, 0, 0, 0, 0, 0, 0, 0]
        b = 0
        c = 0
        for i in range(8):
            c += 2**(7 - i)
            signal = bin2dac(c)
            time.sleep(0.001)
            compvalue = g.input(4)
            if compvalue == 0:
                ar[i] = 0
                c -= 2**(7 - i)
            else:
                ar[i] = 1
                b += 2**(7 - i)
        V = (b / 256) * 3.3
        vol.append(V)
        print("Digital Value : {}, input voltage = {:.2f}".format(b, V))
        mas.append(b)
        n += 1
        #print(ar)
    return n
try:
    start = time.time()
    n = adc()
    end = time.time()
    T = (end - start) / n
    print("Длительность эксперимента = ", end - start)
    print("Период измерений = ", (end - start) / n)
    print("Частота дискретизации = ", 1 / ((end - start) / n))
    masstr = [str(item) for item in mas] 
    with open("/home/gr106/Desktop/Scripts/derevoAM/repo-adc-master/data.txt", "w") as f:
        f.write("\n".join(masstr))
    volstr = [str(item) for item in vol] 
    faa = open("/home/gr106/Desktop/Scripts/derevoAM/repo-adc-master/settings.txt", "w")
    for i in range(n):
        s = str(T * i) + " " + str(vol[i]) + "\n"
        faa.write(s)
    
finally:
    mas = np.array(mas)
    plt.plot(mas)
    plt.show()
    g.output(dac, g.LOW)
    g.cleanup()
