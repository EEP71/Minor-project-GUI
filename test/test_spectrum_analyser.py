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
        value_to_set = 500
        expected_value = f"Pico toolbox confirms that the ADC capture depth is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_capture_depth, value_to_set)
        self.assertEqual(expected_value, real_value, "Test init failed")
        value_to_set = 500000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set))
        self.assertEqual(expected_value, real_value, "Test init failed")

    def test_get_bw_high_enough(self):
        global pico
        value_to_set = 500000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set))
        self.assertEqual(expected_value, real_value, "Test init failed")
        expected_value = 400000 // 2
        real_value = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        real_value = pico._clock_devide_to_sample_rate(real_value) // 2
        self.assertGreater(real_value, expected_value)

    def test_sample_speed_high_enough(self):
        global pico
        value_to_set = 500000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set))
        self.assertEqual(expected_value, real_value, "Test init failed")
        expected_value = 499999
        real_value = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        real_value = pico._clock_devide_to_sample_rate(real_value)
        self.assertGreater(real_value, expected_value)

    def test_resolution_fast_reading_res_50(self):
        global pico
        value_to_set_1 = 50000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set_1}"
        sample_rate = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set_1))
        self.assertEqual(expected_value, sample_rate, "Test init failed")
        value_to_set_2 = 1000
        expected_value = f"Pico toolbox confirms that the ADC capture depth is set to: {value_to_set_2}"
        capture_depth = pico.set_setting(SettingsSelector.set_adc_capture_depth, value_to_set_2)
        self.assertEqual(expected_value, capture_depth, "Test init failed")
        resolution = value_to_set_1 // value_to_set_2
        self.assertLess(resolution, 51)

    def test_resolution_slow_reading_res_10(self):
        global pico
        value_to_set_1 = 25000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set_1}"
        sample_rate = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set_1))
        self.assertEqual(expected_value, sample_rate, "Test init failed")
        value_to_set_2 = 2500
        expected_value = f"Pico toolbox confirms that the ADC capture depth is set to: {value_to_set_2}"
        capture_depth = pico.set_setting(SettingsSelector.set_adc_capture_depth, value_to_set_2)
        self.assertEqual(expected_value, capture_depth, "Test init failed")
        resolution = value_to_set_1 // value_to_set_2
        self.assertLess(resolution, 11)

