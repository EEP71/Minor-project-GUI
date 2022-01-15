import unittest   # The test framework
import serial.tools.list_ports
from pico_com import *
ports = serial.tools.list_ports.comports()



class Test_PicoCom(unittest.TestCase):
    def test_find_com_port(self):
        usb_vid = "USB VID:PID=2E8A:000A"
        usb_serial = "SER=E66"
        how_many_found = 0
        selected_port = 0
        for port, desc, hwid in sorted(ports):
            if usb_vid in hwid:
                if usb_serial in hwid:
                    how_many_found = how_many_found + 1
                    selected_port = str(port)
        self.pico = PicoCom(selected_port)
        if "aaaaa" in self.pico.speedtest_data.decode():
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2, "Not connected to the right devide, or not the right firmware on the Pico")
        self.assertEqual(1, how_many_found, "Multiple RPi Pico's are connected. Not allowed for this test!")

    def test_that(self):
        self.assertEqual(1, 1)