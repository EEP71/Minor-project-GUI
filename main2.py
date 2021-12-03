import tkinter as tk
from tkinter import Image, StringVar, ttk, font as tkfont
from tkinter.constants import *
from PIL import ImageTk, Image

width = 0
height = 0
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
        title.place(x=(width / 2) - (title.winfo_reqwidth() / 2), y=200)

        go_but = tk.Button(self, text = "Go", width=20, command = lambda: self.check_com(), font = controller.button_font)
        go_but.place(x=(width / 2) - (go_but.winfo_reqwidth() / 2) - 220, y=600)

        com_ports = ["COM3", "COM8"]
        self.slected_com = StringVar()
        dropdown = ttk.Combobox(self, width=20, textvariable = self.slected_com, values=com_ports, state="readonly")
        dropdown.place(x=(width / 2) - (dropdown.winfo_reqwidth() / 2) + 220, y=610)

        sub_title = tk.Label(self, text = "Please select a port before continueing", font = controller.paragraph_font)
        sub_title.configure(background="#5E6073")
        sub_title.configure(foreground="#FFFFFF")
        sub_title.place(x=(width / 2) - (sub_title.winfo_reqwidth() / 2), y=850)

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
        title.place(x=(width / 2) - (title.winfo_reqwidth() / 2), y=200)

        awg_but = tk.Button(self, text = "Waveform generator", width=20, command = lambda: self.go_awg(), font = controller.button_font)
        awg_but.place(x=(width / 2) - (awg_but.winfo_reqwidth() / 2) - 200, y=400)

        osc_but = tk.Button(self, text = "Oscilloscope", width=20, command = lambda: self.go_osc(), font = controller.button_font)
        osc_but.place(x=(width / 2) - (osc_but.winfo_reqwidth() / 2) + 200, y=400)

        sa_but = tk.Button(self, text = "Spectrum analyser", width=20, command = lambda: self.go_sa(), font = controller.button_font)
        sa_but.place(x=(width / 2) - (sa_but.winfo_reqwidth() / 2) - 200, y=650)

        lia_but = tk.Button(self, text = "Lock-in amplifier", width=20, command = lambda: self.go_lia(), font = controller.button_font)
        lia_but.place(x=(width / 2) - (lia_but.winfo_reqwidth() / 2) + 200, y=650)    

        back_but = tk.Label(self, text = "Back", font = controller.paragraph_font_u)
        back_but.configure(background="#5E6073")
        back_but.configure(foreground="#F2F4D1")
        back_but.bind("<Button-1>", self.go_back)
        back_but.place(x=(width / 2) - (back_but.winfo_reqwidth() / 2), y=850)

    def go_back(self, event=None):
        self.controller.up_frame("StartPage")

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
    win.deiconify()

if __name__ == "__main__":
    pages = {StartPage, ToolsPage}
    root = tk.Tk()
    root.wm_geometry("1920x1080")
    center(root)
    main = MainView(pages)
    main.mainloop()