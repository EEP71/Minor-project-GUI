import tkinter as tk
from tkinter import Image, StringVar, ttk, font as tkfont
from tkinter.constants import *
from PIL import ImageTk, Image
class MainView(tk.Frame):
    def __init__(self, pages, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=32, weight="bold", slant="roman")
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
        title.pack(side=TOP, fill="x", pady=(250, 10)) 

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.check_com(), font = controller.button_font)
        go_but.pack(side=LEFT, padx=(375, 10))

        com_ports = ["COM3", "COM8"]
        self.slected_com = StringVar()
        dropdown = ttk.Combobox(self, width=20, textvariable = self.slected_com, values=com_ports, state="readonly")
        dropdown.pack(side=RIGHT, padx=(10, 375))

        title = tk.Label(self, text = "Please select a port before continueing", font = controller.paragraph_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#FFFFFF")
        title.place(x=475, y=750)

    def check_com(self):
        value = self.slected_com.get()
        if value != "":
            print(value)
            self.controller.up_frame("ToolsPage")
class ToolsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        title = tk.Label(self, text = "Tool select", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.pack(side=TOP, fill="x", pady=(100, 10))

        awg_but = tk.Button(self, text = "Waveform generator", width=20, command = lambda: self.go_awg(), font = controller.button_font)
        awg_but.place(x=325, y=250)

        osc_but = tk.Button(self, text = "Oscilloscope", width=20, command = lambda: self.go_osc(), font = controller.button_font)
        osc_but.place(x=675, y=250)

        sa_but = tk.Button(self, text = "Spectrum analyser", width=20, command = lambda: self.go_sa(), font = controller.button_font)
        sa_but.place(x=325, y=500)

        lia_but = tk.Button(self, text = "Lock-in amplifier", width=20, command = lambda: self.go_lia(), font = controller.button_font)
        lia_but.place(x=675, y=500)    

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.pack(side=BOTTOM, pady=(0, 50))

    def go_awg(self, event=None):
        self.controller.up_frame("AWG")

    def go_osc(self, event=None):
        self.controller.up_frame("OSC")

    def go_sa(self, event=None):
        self.controller.up_frame("SA")

    def go_lia(self, event=None):
        self.controller.up_frame("LIA")

    def go_back(self, event=None):
        self.controller.up_frame("StartPage")

class AWG(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        title = tk.Label(self, text = "Arbitrary Waveform Generator", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.pack(side=TOP, fill="x", pady=(100, 10))

        wave_type_text = tk.Label(self, text = "Wave Type", font = controller.paragraph_font)
        wave_type_text.configure(background="#5E6073")
        wave_type_text.configure(foreground="#F2F4D1")
        wave_type_text.place(x=250, y=280)

        self.wave_type = tk.Entry(self, width=30)
        self.wave_type.place(x=250, y=310)

        freq_text = tk.Label(self, text = "Frequency", font = controller.paragraph_font)
        freq_text.configure(background="#5E6073")
        freq_text.configure(foreground="#F2F4D1")
        freq_text.place(x=500, y=280)

        self.freq = tk.Entry(self, width=30)
        self.freq.place(x=500, y=310)

        ptp_text = tk.Label(self, text = "Peak To Peak", font = controller.paragraph_font)
        ptp_text.configure(background="#5E6073")
        ptp_text.configure(foreground="#F2F4D1")
        ptp_text.place(x=750, y=280)

        self.ptp = tk.Entry(self, width=30)
        self.ptp.place(x=750, y=310)

        offset_text = tk.Label(self, text = "Offset", font = controller.paragraph_font)
        offset_text.configure(background="#5E6073")
        offset_text.configure(foreground="#F2F4D1")
        offset_text.place(x=250, y=480)

        self.offset = tk.Entry(self, width=30)
        self.offset.place(x=250, y=510)

        channel_nmr_text = tk.Label(self, text = "Channel Number", font = controller.paragraph_font)
        channel_nmr_text.configure(background="#5E6073")
        channel_nmr_text.configure(foreground="#F2F4D1")
        channel_nmr_text.place(x=500, y=480)

        self.channel_nmr = tk.Entry(self, width=30)
        self.channel_nmr.place(x=500, y=510)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.print(), font = controller.button_font)
        go_but.configure(background="#B2D3BE")
        go_but.place(x=750, y=500)

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.pack(side=BOTTOM, pady=(0, 50))

    def print(self, event=None):
        wave_type = self.wave_type.get()
        freq = self.freq.get()
        ptp = self.ptp.get()
        offset = self.offset.get()
        channel_nmr = self.channel_nmr.get()
        if wave_type != "" or freq != "" or ptp != "" or offset != "" or channel_nmr != "":
            print("Wave Type: " + wave_type + "\nFrequency: " + freq + "\nPeak To Peak: " + ptp + "\nOffset: " + offset + "\nChannel number: " + channel_nmr)

    def go_back(self, event=None):
        self.controller.up_frame("ToolsPage")

class OSC(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        title = tk.Label(self, text = "Oscilloscope", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.pack(side=TOP, fill="x", pady=(100, 10))

        sample_rate_text = tk.Label(self, text = "Sample Rate", font = controller.paragraph_font)
        sample_rate_text.configure(background="#5E6073")
        sample_rate_text.configure(foreground="#F2F4D1")
        sample_rate_text.place(x=250, y=360)

        self.sample_rate = tk.Entry(self, width=30)
        self.sample_rate.place(x=250, y=390)

        amp_text = tk.Label(self, text = "Amplification", font = controller.paragraph_font)
        amp_text.configure(background="#5E6073")
        amp_text.configure(foreground="#F2F4D1")
        amp_text.place(x=500, y=360)

        self.amp = tk.Entry(self, width=30)
        self.amp.place(x=500, y=390)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.print(), font = controller.button_font)
        go_but.configure(background="#B2D3BE")
        go_but.place(x=750, y=380)

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.pack(side=BOTTOM, pady=(0, 50))

    def print(self, event=None):
        sample_rate = self.sample_rate.get()
        amp = self.amp.get()
        if sample_rate != "" or amp != "":
            print("Sample Rate: " + sample_rate + "\nAmplification: " + amp)

    def go_back(self, event=None):
        self.controller.up_frame("ToolsPage")

class SA(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        title = tk.Label(self, text = "Spectrum Analyser", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.pack(side=TOP, fill="x", pady=(100, 10))

        sample_rate_text = tk.Label(self, text = "Sample Rate", font = controller.paragraph_font)
        sample_rate_text.configure(background="#5E6073")
        sample_rate_text.configure(foreground="#F2F4D1")
        sample_rate_text.place(x=250, y=360)

        self.sample_rate = tk.Entry(self, width=30)
        self.sample_rate.place(x=250, y=390)

        fft_size_text = tk.Label(self, text = "FFT Size", font = controller.paragraph_font)
        fft_size_text.configure(background="#5E6073")
        fft_size_text.configure(foreground="#F2F4D1")
        fft_size_text.place(x=500, y=360)

        self.fft_size = tk.Entry(self, width=30)
        self.fft_size.place(x=500, y=390)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.print(), font = controller.button_font)
        go_but.configure(background="#B2D3BE")
        go_but.place(x=750, y=380)

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.pack(side=BOTTOM, pady=(0, 50))

    def print(self, event=None):
        sample_rate = self.sample_rate.get()
        fft_size = self.fft_size.get()
        if sample_rate != "" or fft_size != "":
            print("Sample Rate: " + sample_rate + "\nFFT Size: " + fft_size)

    def go_back(self, event=None):
        self.controller.up_frame("ToolsPage")

class LIA(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        title = tk.Label(self, text = "Lock-in Amplifier", font = controller.title_font)
        title.configure(background="#5E6073")
        title.configure(foreground="#F2F4D1")
        title.pack(side=TOP, fill="x", pady=(100, 10))

        base_freq_text = tk.Label(self, text = "Base Frequency", font = controller.paragraph_font)
        base_freq_text.configure(background="#5E6073")
        base_freq_text.configure(foreground="#F2F4D1")
        base_freq_text.place(x=250, y=360)

        self.base_freq = tk.Entry(self, width=30)
        self.base_freq.place(x=250, y=390)

        lpf_cut_off_text = tk.Label(self, text = "LPF cut-off Frequency", font = controller.paragraph_font)
        lpf_cut_off_text.configure(background="#5E6073")
        lpf_cut_off_text.configure(foreground="#F2F4D1")
        lpf_cut_off_text.place(x=500, y=360)

        self.lpf_cut_off = tk.Entry(self, width=30)
        self.lpf_cut_off.place(x=500, y=390)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.print(), font = controller.button_font)
        go_but.configure(background="#B2D3BE")
        go_but.place(x=750, y=380)

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.pack(side=BOTTOM, pady=(0, 50))

    def print(self, event=None):
        base_freq = self.base_freq.get()
        lpf_cut_off = self.lpf_cut_off.get()
        if base_freq != "" or lpf_cut_off != "":
            print("Base Frequency: " + base_freq + "\nLPF cut-off Frequency: " + lpf_cut_off)

    def go_back(self, event=None):
        self.controller.up_frame("ToolsPage")

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

if __name__ == "__main__":
    pages = {StartPage, ToolsPage, AWG, OSC, SA, LIA}
    root = tk.Tk()
    main = MainView(pages)
    root.wm_geometry("1200x800")
    center(root)
    main.mainloop()