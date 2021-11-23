import wx

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Pico Test Equipment', size=(750, 750))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self.cb_label = wx.StaticText(panel,label = "Select an option:", style = wx.ALIGN_CENTER) 
        box.Add(self.cb_label, 0, wx.ALL | wx.EXPAND, 5)

        self.combo = wx.ComboBox(panel,choices = ['test1', 'test2', 'test3']) 
        self.combo.Bind(wx.EVT_COMBOBOX, self.on_combo)
        box.Add(self.combo, 0, wx.ALL | wx.CENTER, 5)

        self.input = wx.SpinCtrl(panel)
        box.Add(self.input, 0, wx.ALL | wx.CENTER, 5)

        self.btn = wx.Button(panel, label='Press Me')
        self.btn.Bind(wx.EVT_BUTTON, self.on_button_press)
        box.Add(self.btn, 0, wx.ALL | wx.CENTER, 5)

        self.rb1 = wx.RadioButton(panel, 11, label = 'Value A', pos = (10,10), style = wx.RB_GROUP) 
        self.rb2 = wx.RadioButton(panel, 22, label = 'Value B', pos = (10,40)) 
        self.rb3 = wx.RadioButton(panel, 33, label = 'Value C', pos = (10,70))
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_press)
        box.Add(self.rb1, 0, wx.ALL | wx.CENTER) 
        box.Add(self.rb2, 0, wx.ALL | wx.CENTER) 
        box.Add(self.rb3, 0, wx.ALL | wx.CENTER) 

        panel.SetSizer(box)
        self.Center()
        self.Show()

    def on_button_press(self, event):
        value = self.input.GetValue()
        print(value)

    def on_radio_press(self, event):
        rb = event.GetEventObject()
        print(rb.GetLabel())

    def on_combo(self, event): 
        value = self.combo.GetValue()
        print(value)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()