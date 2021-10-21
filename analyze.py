import matplotlib.pyplot as plt
import numpy as np
with open("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")]
    #print(tmp)

y = np.loadtxt("data.txt", dtype = int)
y = y * tmp[1]
x = np.arange(0, tmp[0] * (len(y)), tmp[0])
#print(data_array)

x1 = []
y1 = []
i = 0
while i < len(x):
    x1.append(x[i])
    y1.append(y[i])
    i += 100
#print(x1)
fig, ax = plt.subplots(figsize=(16, 10), dpi = 200)
fig.suptitle("Процес зарядки и разрядки конденсатора в RC цепи")
ax.plot(x, y, lw = 0.5)
ax.scatter(x1, y1, s = 3)
plt.xlabel("Время, с")
plt.ylabel("Напряжение, В")
plt.text(30, 1.2, "Время зарядки = 49.3с")
plt.text(30, 0.75, "Время разрядки = 40.7с")
plt.grid(True, which = "major", linestyle = "-")
plt.minorticks_on()
plt.grid(True, which = "minor", linestyle = "--", alpha = 0.2)
ax.axis([0, 90, 0, 3.5])
fig.savefig("gr.png")
plt.show()