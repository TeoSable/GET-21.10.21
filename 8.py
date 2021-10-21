import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

data = np.loadtxt("data.txt", dtype = float)
settings = np.loadtxt("settings.txt", dtype = float)
voltage = settings[0]
period = settings[1]

timeline = np.arange(0, period * len(data), period)

fig, ax = plt.subplots(figsize = (16,10), dpi = 200)

ax.grid(color = '0.5', linestyle = '-', which = 'major')
ax.grid(color = '0.8', linestyle = '--', which = 'minor')

ax.plot(timeline, data * voltage, linestyle = "-", linewidth = "1", marker = "o", markeredgecolor = 'C1', markerfacecolor = 'w', markevery = 200, markersize = 4)

ax.set_title("Процесс зарядки и разрядки конденсатора в RC-цепочке", wrap = 'true')
ax.set_ylabel("U, В")
ax.set_xlabel("t, с")

ax.text(60, 2.6, r"Время зарядки - {:.2f} c".format(timeline[np.argmax(data)]), fontsize = 'large', wrap = 'true', color = '0.2')
ax.text(60, 2.1, r"Время разрядки - {:.2f} c".format(max(timeline) - timeline[np.argmax(data)]), fontsize = 'large', wrap = 'true', color = '0.2')
ax.legend(["U(t)"])

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

ax.set_xlim(0, max(timeline))
ax.set_ylim(0, max(data * voltage))

fig.savefig('graph.svg')
plt.show()

