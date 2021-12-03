# import
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# signal generation
N = 10001
stop = 100
time = np.linspace(0, stop, N)
A = 1/4*np.cos(2*np.pi*(np.abs(time - stop/2)/stop)) + 1
f = np.concatenate((1*np.ones(int(N/4)), 2*np.ones(int(N/2) + 1), 1*np.ones(int(N/4))))
signal = A * np.sin(2*np.pi*f*time) + 0.05*np.random.randn(N)

# figure preparation
fig, ax = plt.subplots(1, 1, figsize = (8*0.9, 6*0.9))
displayed_period = int(2*f.min())
span = int(N/stop/f.min())

def animation(i):
    # delete previous frame
    ax.cla()

    # plot and set axes limits
    ax.plot(time[span*i: 1 + span*(i + displayed_period)],
            signal[span*i: 1 + span*(i + displayed_period)])
    ax.set_xlim([time[span*i], time[span*(i + displayed_period)]])
    ax.set_ylim([1.1*signal.min(), 1.1*signal.max()])

# run animation
anim = FuncAnimation(fig, animation, frames = int(len(time)/span - 1), interval = 10)
plt.show()