# import
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# signal generation
sample_amount = 10001
stop = 100
time = np.linspace(0, stop, sample_amount)
amplitude = 1/4 * np.cos(2 * np.pi * (np.abs(time - stop / 2) / stop)) + 1
frequency = np.concatenate((1 * np.ones(int(sample_amount/4)), 2 * np.ones(int(sample_amount/2) + 1), 1 * np.ones(int(sample_amount/4))))
signal = amplitude * np.sin(2 * np.pi * frequency * time)  + 0.05 * np.random.randn(sample_amount)

# figure preparation
fig, ax = plt.subplots(1, 1, figsize = (8 * 0.9, 6 * 0.9))
displayed_period = int(2 * frequency.min())
span = int(sample_amount / stop / frequency.min())

def animation(i):
    # delete previous frame
    ax.cla()

    # plot and set axes limits
    ax.plot(time[span * i: 1 + span * (i + displayed_period)],
            signal[span * i: 1 + span * (i + displayed_period)])
    ax.set_xlim([time[span*i], time[span*(i + displayed_period)]])
    ax.set_ylim([1.1*signal.min(), 1.1*signal.max()])

# run animation
anim = FuncAnimation(fig, animation, frames = int(len(time) / span - 1), interval = 10)
plt.show()