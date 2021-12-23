import tkinter as tk
from tkinter import Image, StringVar, ttk, font as tkfont
from tkinter.constants import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation
# from PIL import ImageTk, Image

import numpy as np
from numpy import arange, sin, pi
from numpy.lib.function_base import select

import serial.tools.list_ports

from pico_com import *

canvas = None

width = 0
height = 0

tool_one = ""
tool_two = ""

root = None
pico = None

#######SPECTRUM ANALUZER GLOBALS#########
sa_capture_depth = 1000  #This is the default value of the pico
sa_sample_rate   = 50000 #This is the default value of the pico

#########################################

class MainView(tk.Frame):
    def __init__(self, pages, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.line_style = ttk.Style()
        self.line_style.configure("Line.TSeparator", background="#000000")

        self.title_font = tkfont.Font(family='Calibri', size=32, weight="bold", slant="roman")
        self.title_small_font = tkfont.Font(family='Calibri', size=24, weight="bold", slant="roman")
        self.paragraph_font = tkfont.Font(family='Calibri', size=14, slant="roman")
        self.paragraph_font_u = tkfont.Font(family='Calibri', size=14, underline=True, slant="roman")
        self.button_font = tkfont.Font(family='Calibri', size=16, slant="roman")

        container = tk.Frame()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.id = tk.StringVar()
        self.id.set("PTE")

        self.listing = {}

        for page in (pages):
            page_name = page.__name__
            frame = page(parent = container, controller = self)
            frame.grid(row=0, column=0, sticky="nesw")
            frame.configure(background="#5E6073")
            self.listing[page_name] = frame

        self.up_frame('StartPage')

    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        # rendered_logo = ImageTk.PhotoImage(Image.open("images/logo.png"))
        # label = tk.Label(self, image = rendered_logo)
        # label.configure(background="#5E6073")
        # label.pack()

        title = tk.Label(self, text = "Pico Test Equipment", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.place(x=(width / 2) - (title.winfo_reqwidth() / 2), y=200)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.check_com(), font = controller.button_font)
        go_but.place(x=(width / 2) - (go_but.winfo_reqwidth() / 2) - 220, y=600)


        ports = serial.tools.list_ports.comports()
        com_ports = []
        for port, desc, hwid in sorted(ports):
            com_ports.append("{}".format(port))
        self.slected_com = StringVar()
        dropdown = ttk.Combobox(self, width=20, textvariable = self.slected_com, values=com_ports, state="readonly")
        dropdown.place(x=(width / 2) - (dropdown.winfo_reqwidth() / 2) + 220, y=610)

        sub_title = tk.Label(self, text = "Please select a port before continueing", font = controller.paragraph_font)
        sub_title.configure(background="#5E6073")
        sub_title.configure(foreground="#FFFFFF")
        sub_title.place(x=(width / 2) - (sub_title.winfo_reqwidth() / 2), y=850)

    def check_com(self):
        global pico
        selected_com = self.slected_com.get()
        if selected_com != "":
            pico = PicoCom(str(selected_com))
            self.controller.up_frame("MainPage")
            canvas.get_tk_widget().place(x=0, y=0, height=1050, width=1595)

class MainPage(tk.Frame):
    global sa_capture_depth
    global sa_sample_rate
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        seperator = ttk.Separator(self, orient='vertical', style="Line.TSeparator")
        seperator.place(x=(width / 2) - (seperator.winfo_reqwidth() / 2) + 635, rely=0, width=5, relheight=1)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Graph

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        line = plt.plot([],[])[0]

        label = ax.text(0, 0, "HIGHEST FREQ:", ha='left', va='top', fontsize=20, color="Red")
        def init_line():
            line.set_data(0, 0)
            return (line,)

        def animate(i):
            global x
            global pico
            if pico is not None:
                x = range(0,int(sa_sample_rate/2),int(sa_sample_rate/sa_capture_depth))
                if (len(pico.get_SA_values()) == len(x)) and pico is not None:
                    line.set_data(x, pico.get_SA_values())
                    highest_amp = np.argmax(pico.get_SA_values())
                    label.set_text(f"HIGHEST FREQ: {x[highest_amp]}")
                else:
                    line.set_data(0, 0)
            else:
                line.set_data(0, 0)
            return line, label,

        global canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        # plt.xlim(0, 500000/2+1) ## THIS IS THE MAX WINDOW FOR DE INTERNAL ADC
        plt.xlim(0, sa_sample_rate/2+1)
        plt.ylim(-50, 40)
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.title('Spectrum analyser')
        plt.autoscale(enable=True, axis='x')
        self.ani =  matplotlib.animation.FuncAnimation(fig, animate, init_func=init_line, interval=25, blit=True)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Start tool 1

        self.tools_one = ["None", "Arbitrary Waveform Generator", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]
        self.slected_tool_one = StringVar(value=self.tools_one[0])
        self.dropdown_one = ttk.Combobox(self, width=38, textvariable = self.slected_tool_one, values=self.tools_one, state="readonly")
        self.dropdown_one.place(x=(width / 2) - (self.dropdown_one.winfo_reqwidth() / 2) + 800, y=0)
        self.dropdown_one.bind("<<ComboboxSelected>>", self.check_tool_one)

        self.title_one = tk.Label(self, text = "Select a tool", font = controller.title_small_font)
        self.title_one.configure(background="#5E6073")
        self.title_one.configure(foreground="#F2F4D1")
        self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# AWG
        self.wave_type_text = tk.Label(self, text = "Wave Type", font = controller.paragraph_font)
        self.wave_type_text.configure(background="#5E6073")
        self.wave_type_text.configure(foreground="#F2F4D1")

        self.wave_type = tk.Entry(self, width=30)

        self.freq_text = tk.Label(self, text = "Frequency", font = controller.paragraph_font)
        self.freq_text.configure(background="#5E6073")
        self.freq_text.configure(foreground="#F2F4D1")

        self.freq = tk.Entry(self, width=30)

        self.ptp_text = tk.Label(self, text = "Peak To Peak", font = controller.paragraph_font)
        self.ptp_text.configure(background="#5E6073")
        self.ptp_text.configure(foreground="#F2F4D1")

        self.ptp = tk.Entry(self, width=30)

        self.offset_text = tk.Label(self, text = "Offset", font = controller.paragraph_font)
        self.offset_text.configure(background="#5E6073")
        self.offset_text.configure(foreground="#F2F4D1")

        self.offset = tk.Entry(self, width=30)

        self.channel_nmr_text = tk.Label(self, text = "Channel Number", font = controller.paragraph_font)
        self.channel_nmr_text.configure(background="#5E6073")
        self.channel_nmr_text.configure(foreground="#F2F4D1")

        self.channel_nmr = tk.Entry(self, width=30)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# OSC
        self.amp_text = tk.Label(self, text = "Amplification", font = controller.paragraph_font)
        self.amp_text.configure(background="#5E6073")
        self.amp_text.configure(foreground="#F2F4D1")

        amp_values = ["100x", "10x", "1x", "0.1x"]
        self.slected_amp = StringVar()
        self.amp = ttk.Combobox(self, width=30, textvariable = self.slected_amp, values=amp_values, state="readonly")

        self.trigger_text = tk.Label(self, text = "Trigger level", font = controller.paragraph_font)
        self.trigger_text.configure(background="#5E6073")
        self.trigger_text.configure(foreground="#F2F4D1")

        self.trigger = tk.Entry(self, width=30)

        self.direction_text = tk.Label(self, text = "Direction", font = controller.paragraph_font)
        self.direction_text.configure(background="#5E6073")
        self.direction_text.configure(foreground="#F2F4D1")

        dir_values = ["0", "1"]
        self.selected_dir = StringVar()
        self.direction = ttk.Combobox(self, width=30, textvariable = self.selected_dir, values=dir_values, state="readonly")

        self.sd_text_osc = tk.Label(self, text = "Seconds per division", font = controller.paragraph_font)
        self.sd_text_osc.configure(background="#5E6073")
        self.sd_text_osc.configure(foreground="#F2F4D1")

        self.sd_osc = tk.Entry(self, width=30)

        self.vd_text_osc = tk.Label(self, text = "Voltage per division", font = controller.paragraph_font)
        self.vd_text_osc.configure(background="#5E6073")
        self.vd_text_osc.configure(foreground="#F2F4D1")

        self.vd_osc = tk.Entry(self, width=30)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# LIA
        self.base_freq_text = tk.Label(self, text = "Base Frequency", font = controller.paragraph_font)
        self.base_freq_text.configure(background="#5E6073")
        self.base_freq_text.configure(foreground="#F2F4D1")

        self.base_freq = tk.Entry(self, width=30)

        self.lpf_cut_off_text = tk.Label(self, text = "LPF cut-off Frequency", font = controller.paragraph_font)
        self.lpf_cut_off_text.configure(background="#5E6073")
        self.lpf_cut_off_text.configure(foreground="#F2F4D1")

        self.lpf_cut_off = tk.Entry(self, width=30)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# SA
        self.sample_rate_text = tk.Label(self, text = "Sample Rate", font = controller.paragraph_font)
        self.sample_rate_text.configure(background="#5E6073")
        self.sample_rate_text.configure(foreground="#F2F4D1")

        self.sample_rate = tk.Entry(self, width=30)

        self.fft_size_text = tk.Label(self, text = "FFT Size", font = controller.paragraph_font)
        self.fft_size_text.configure(background="#5E6073")
        self.fft_size_text.configure(foreground="#F2F4D1")

        self.fft_size = tk.Entry(self, width=30)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# End tool 1
        self.but_one = tk.Button(self, text = "Start", width=20, command = lambda: self.start_one(), font = controller.button_font)
        self.but_one.configure(background="#B2D3BE")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Start tool 2
        self.tools_two = ["None", "Arbitrary Waveform Generator", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]
        self.slected_tool_two = StringVar(value=self.tools_two[0])
        self.dropdown_two = ttk.Combobox(self, width=38, textvariable = self.slected_tool_two, values=self.tools_one, state="readonly")
        self.dropdown_two.place(x=(width / 2) - (self.dropdown_two.winfo_reqwidth() / 2) + 800, y=height / 2)
        self.dropdown_two.bind("<<ComboboxSelected>>", self.check_tool_two)

        self.title_two = tk.Label(self, text = "Select a tool", font = controller.title_small_font)
        self.title_two.configure(background="#5E6073")
        self.title_two.configure(foreground="#F2F4D1")
        self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height / 2 + 35)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# End tool 2

        self.but_two = tk.Button(self, text = "Start", width=20, command = lambda: self.start_two(), font = controller.button_font)
        self.but_two.configure(background="#B2D3BE")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def check_tool_one(self, event=None):
        value = self.slected_tool_one.get()
        self.but_one.place(x=(width / 2) - (self.but_one.winfo_reqwidth() / 2) + 800, y=height / 2 - 60)
        if value == "None":
            self.dropdown_two['values'] = ["None", "Arbitrary Waveform Generator", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]

            self.title_one.config(text="Select a tool")
            self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

            self.but_one.place(x=-200, y=-200)
            self.swap_buttons("none", 0)
        elif value == "Arbitrary Waveform Generator":
            self.dropdown_two['values'] = ["None", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]

            self.title_one.config(text="Arbitrary Waveform\n Generator")
            self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

            self.swap_buttons("awg", 0)
        else:
            self.dropdown_two['values'] = ["None", "Arbitrary Waveform Generator"]

            if value == "Oscilloscope":
                self.title_one.config(text="Oscilloscope")
                self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

                self.swap_buttons("osc", 0)
            elif value == "Lock-in Amplifier":
                self.title_one.config(text="Lock-in Amplifier")
                self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

                self.swap_buttons("lia", 0)
            elif value == "Spectrum Analyser":
                self.title_one.config(text="Spectrum Analyser")
                self.title_one.place(x=(width / 2) - (self.title_one.winfo_reqwidth() / 2) + 800, y=35)

                self.swap_buttons("sa", 0)

    def check_tool_two(self, event=None):
        value = self.slected_tool_two.get()
        self.but_two.place(x=(width / 2) - (self.but_two.winfo_reqwidth() / 2) + 800, y=height - 100)
        if value == "None":
            self.dropdown_one['values'] = ["None", "Arbitrary Waveform Generator", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]

            self.title_two.config(text="Select a tool")
            self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height/2 + 35)

            self.but_two.place(x=-200, y=-200)
            self.swap_buttons("none", 1)
        elif value == "Arbitrary Waveform Generator":
            self.dropdown_one['values'] = ["None", "Oscilloscope", "Lock-in Amplifier", "Spectrum Analyser"]

            self.title_two.config(text="Arbitrary Waveform\n Generator")
            self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height/2 + 35)

            self.swap_buttons("awg", 1)
        else:
            self.dropdown_one['values'] = ["None", "Arbitrary Waveform Generator"]

            if value == "Oscilloscope":
                self.title_two.config(text="Oscilloscope")
                self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height/2 + 35)

                self.swap_buttons("osc", 1)
            elif value == "Lock-in Amplifier":
                self.title_two.config(text="Lock-in Amplifier")
                self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height/2 + 35)

                self.swap_buttons("lia", 1)
            elif value == "Spectrum Analyser":
                self.title_two.config(text="Spectrum Analyser")
                self.title_two.place(x=(width / 2) - (self.title_two.winfo_reqwidth() / 2) + 800, y=height/2 + 35)

                self.swap_buttons("sa", 1)

    def start_one(self):
        global tool_one
        global pico
        global sa_capture_depth
        global sa_sample_rate
        if self.but_one["text"] == "Start":
            self.but_one.config(background="#EA7870", text="Stop")
            if tool_one == "sa":
                try:
                    fft_value = int(self.fft_size.get())
                    sample_rate = int(self.sample_rate.get())
                    print(f"MESSAGE FROM PICO: {pico.set_setting(SettingsSelector.set_adc_sample_rate, sample_rate)}")
                    print(f"MESSAGE FROM PICO: {pico.set_setting(SettingsSelector.set_adc_capture_depth, fft_value)}")
                    sa_sample_rate = int(pico.get_setting(SettingsSelector.get_adc_sample_rate))
                    sa_capture_depth = int(pico.get_setting(SettingsSelector.get_adc_capture_depth))
                    print(f"MESSAGE FROM PICO: Get adc caputre depth = {sa_capture_depth}")
                    print(f"MESSAGE FROM PICO: Get adc sample rate {sa_sample_rate}")
                    pico.set_capture_depth(sa_capture_depth)
                    pico.set_tool(ToolSelector.SA)
                except:
                    print("VALUE IS NOT A FUCKING INT THIS TRY EXPECT SUCKS BTW CHANGE iT TO CHECK IF VALUES ARE INT NOT CHARACTERS")

        else:
            self.but_one.config(background="#B2D3BE", text="Start")
            pico.set_tool(ToolSelector.no_tool)

    def start_two(self):
        if self.but_two["text"] == "Start":
            self.but_two.config(background="#EA7870", text="Stop")
        else:
            self.but_two.config(background="#B2D3BE", text="Start")

    def swap_buttons(self, tool, side):
        global tool_one
        global tool_two

        if side == 0:
            tool_one = tool
        else:
            tool_two = tool

        if tool_one != "awg" and tool_two != "awg":
            self.wave_type_text.place(x=-200, y=-200)
            self.wave_type.place(x=-200, y=-200)
            self.freq_text.place(x=-200, y=-200)
            self.freq.place(x=-200, y=-200)
            self.ptp_text.place(x=-200, y=-200)
            self.ptp.place(x=-200, y=-200)
            self.offset_text.place(x=-200, y=-200)
            self.offset.place(x=-200, y=-200)
            self.channel_nmr_text.place(x=-200, y=-200)
            self.channel_nmr.place(x=-200, y=-200)

        if tool_one != "osc" and tool_two != "osc":
            self.amp_text.place(x=-200, y=-200)
            self.amp.place(x=-200, y=-200)
            self.trigger_text.place(x=-200, y=-200)
            self.trigger.place(x=-200, y=-200)
            self.direction_text.place(x=-200, y=-200)
            self.direction.place(x=-200, y=-200)
            self.sd_text_osc.place(x=-200, y=-200)
            self.sd_osc.place(x=-200, y=-200)
            self.vd_text_osc.place(x=-200, y=-200)
            self.vd_osc.place(x=-200, y=-200)

        if tool_one != "lia" and tool_two != "lia":
            self.base_freq_text.place(x=-200, y=-200)
            self.base_freq.place(x=-200, y=-200)
            self.lpf_cut_off_text.place(x=-200, y=-200)
            self.lpf_cut_off.place(x=-200, y=-200)

        if tool_two != "sa" and tool_two != "sa":
            self.sample_rate_text.place(x=-200, y=-200)
            self.sample_rate.place(x=-200, y=-200)
            self.fft_size_text.place(x=-200, y=-200)
            self.fft_size.place(x=-200, y=-200)

        if tool == "awg":
            self.wave_type_text.place(x=(width / 2) - (self.wave_type_text.winfo_reqwidth() / 2) + 800, y=130 + height / 2 * side)
            self.wave_type.place(x=(width / 2) - (self.wave_type.winfo_reqwidth() / 2) + 800, y=160 + height / 2 * side)
            self.freq_text.place(x=(width / 2) - (self.freq_text.winfo_reqwidth() / 2) + 800, y=190 + height / 2 * side)
            self.freq.place(x=(width / 2) - (self.freq.winfo_reqwidth() / 2) + 800, y=220 + height / 2 * side)
            self.ptp_text.place(x=(width / 2) - (self.ptp_text.winfo_reqwidth() / 2) + 800, y=250 + height / 2 * side)
            self.ptp.place(x=(width / 2) - (self.ptp.winfo_reqwidth() / 2) + 800, y=280 + height / 2 * side)
            self.offset_text.place(x=(width / 2) - (self.offset_text.winfo_reqwidth() / 2) + 800, y=310 + height / 2 * side)
            self.offset.place(x=(width / 2) - (self.offset.winfo_reqwidth() / 2) + 800, y=340 + height / 2 * side)
            self.channel_nmr_text.place(x=(width / 2) - (self.channel_nmr_text.winfo_reqwidth() / 2) + 800, y=370 + height / 2 * side)
            self.channel_nmr.place(x=(width / 2) - (self.channel_nmr.winfo_reqwidth() / 2) + 800, y=400 + height / 2 * side)
        elif tool == "osc":
            self.amp_text.place(x=(width / 2) - (self.amp_text.winfo_reqwidth() / 2) + 800, y=130 + height / 2 * side)
            self.amp.place(x=(width / 2) - (self.amp.winfo_reqwidth() / 2) + 800, y=160 + height / 2 * side)
            self.trigger_text.place(x=(width / 2) - (self.trigger_text.winfo_reqwidth() / 2) + 800, y=190 + height / 2 * side)
            self.trigger.place(x=(width / 2) - ( self.trigger.winfo_reqwidth() / 2) + 800, y=220 + height / 2 * side)
            self.direction_text.place(x=(width / 2) - (self.direction_text.winfo_reqwidth() / 2) + 800, y=250 + height / 2 * side)
            self.direction.place(x=(width / 2) - ( self.direction.winfo_reqwidth() / 2) + 800, y=280 + height / 2 * side)
            self.sd_text_osc.place(x=(width / 2) - (self.sd_text_osc.winfo_reqwidth() / 2) + 800, y=310 + height / 2 * side)
            self.sd_osc.place(x=(width / 2) - ( self.sd_osc.winfo_reqwidth() / 2) + 800, y=340 + height / 2 * side)
            self.vd_text_osc.place(x=(width / 2) - (self.vd_text_osc.winfo_reqwidth() / 2) + 800, y=370 + height / 2 * side)
            self.vd_osc.place(x=(width / 2) - ( self.vd_osc.winfo_reqwidth() / 2) + 800, y=400 + height / 2 * side)
        elif tool == "lia":
            self.base_freq_text.place(x=(width / 2) - (self.base_freq_text.winfo_reqwidth() / 2) + 800, y=130 + height / 2 * side)
            self.base_freq.place(x=(width / 2) - (self.base_freq.winfo_reqwidth() / 2) + 800, y=160 + height / 2 * side)
            self.lpf_cut_off_text.place(x=(width / 2) - (self.lpf_cut_off_text.winfo_reqwidth() / 2) + 800, y=190 + height / 2 * side)
            self.lpf_cut_off.place(x=(width / 2) - (self.lpf_cut_off.winfo_reqwidth() / 2) + 800, y=220 + height / 2 * side)
        elif tool == "sa":
            self.sample_rate_text.place(x=(width / 2) - (self.sample_rate_text.winfo_reqwidth() / 2) + 800, y=130 + height / 2 * side)
            self.sample_rate.place(x=(width / 2) - (self.sample_rate.winfo_reqwidth() / 2) + 800, y=160 + height / 2 * side)
            self.fft_size_text.place(x=(width / 2) - (self.fft_size_text.winfo_reqwidth() / 2) + 800, y=190 + height / 2 * side)
            self.fft_size.place(x=(width / 2) - (self.fft_size.winfo_reqwidth() / 2) + 800, y=220 + height / 2 * side)

def center(win):
    win.update_idletasks()

    global width
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    global height
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    # win.geometry(f'{width}x{height}+{x}+{y}')
    win.deiconify()

def init_gui(width, height, title):
    global root
    root = tk.Tk()
    root.wm_geometry(str(width) + "x" + str(height))
    root.wm_title(title)
    center(root)