import gui

if __name__ == "__main__":
    gui.init_gui(1920, 1080, "Pico Test Equipment")

    pages = {gui.StartPage, gui.MainPage}
    main = gui.MainView(pages)
    main.mainloop()