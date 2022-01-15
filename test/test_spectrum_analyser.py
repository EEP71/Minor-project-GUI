import unittest   # The test framework
import serial.tools.list_ports
from pico_com import *
ports = serial.tools.list_ports.comports()

pico = None
class test_SpectrumAnalyser(unittest.TestCase):
    def test_find_com_port(self):
        global pico
        usb_vid = "USB VID:PID=2E8A:000A"
        usb_serial = "SER=E66"
        how_many_found = 0
        selected_port = 0
        for port, desc, hwid in sorted(ports):
            if usb_vid in hwid:
                if usb_serial in hwid:
                    how_many_found = how_many_found + 1
                    selected_port = str(port)
        pico = PicoCom(selected_port)
        if "aaaaa" in pico.speedtest_data.decode():
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2, "Not connected to the right devide, or not the right firmware on the Pico")
        self.assertEqual(1, how_many_found, "Multiple RPi Pico's are connected. Not allowed for this test!")

    def test_get_bw_high_enough(self):
        global pico
        pico.set_setting(SettingsSelector.set_adc_capture_depth, 500000)
        clock_devide = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        sample_rate = pico._clock_devide_to_sample_rate(clock_devide)
        self.assertGreater(sample_rate, 400000, "Bandwith is not high enough")

    def test_sample_speed(self):
        global pico
        expected_value = 960
        sample_rate = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        self.assertEqual(1, 1)

    def test_resolution(self):
        global pico
        expected_value = 960
        sample_rate = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        self.assertEqual(1, 1)