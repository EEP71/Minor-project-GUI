# import
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import time

# signal generation
sample_amount = 10001
stop = 100
time = np.linspace(0, stop, sample_amount)
amplitude = 1/4 * np.cos(2 * np.pi * (np.abs(time - stop / 2) / stop)) + 1
frequency = np.concatenate((1 * np.ones(int(sample_amount/4)), 2 * np.ones(int(sample_amount/2) + 1), 1 * np.ones(int(sample_amount/4))))
signal = amplitude * np.sin(2 * np.pi * frequency * time)  + 0.05 * np.random.randn(sample_amount)

# color definition
black = '#0F110D'
grey = '#3B3D3a'
yellow = '#FFFF21'

# figure preparation
fig, ax = plt.subplots(1, 1, figsize = (8 * 0.9, 6 * 0.9))
displayed_period = int(2 * frequency.min())
span = int(sample_amount / stop / frequency.min())

def animation(i):
    # delete previous frame
    ax.cla()

    # set background color and plot line
    ax.set_facecolor(black)
    ax.plot(time[span * i: 1 + span * (i + displayed_period)],
            signal[span * i: 1 + span * (i + displayed_period)],
            color = yellow)

    # plot axes lines
    ax.hlines(y = 0,
              xmin = 0,
              xmax = stop,
              lw = 2,
              colors = grey)
    ax.vlines(x = time[int(span * i + (1 + span * displayed_period) / 2)],
              ymin = 1.1 * signal.min(),
              ymax = 1.1 * signal.max(),
              lw = 2,
              colors = grey)

    # set grid, axes limits and ticks
    ax.grid(which = 'major',
            ls = '-',
            lw = 0.5,
            color = grey)
    ax.set_xlim([time[span * i], time[span * (i + displayed_period)]])
    ax.set_ylim([1.1 * signal.min(), 1.1 * signal.max()])
    
    plt.tick_params(axis = 'both',
                    which = 'both',
                    bottom = False,
                    left = False,
                    labelbottom = False,
                    labelleft = False)

# run animation
anim = FuncAnimation(fig, animation, frames = int(len(time) / span - 1), interval = 10)
plt.show()