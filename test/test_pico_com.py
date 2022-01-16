import unittest   # The test framework
import serial.tools.list_ports
from pico_com import *
ports = serial.tools.list_ports.comports()

pico = None
class Test_PicoCom(unittest.TestCase):
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

    def test_sample_rate_to_clock_devide(self):
        global pico
        self.assertEqual(pico._sample_rate_to_clock_devide(500000), 96)

    def test_set_adc_capture_depth(self):
        global pico
        value_to_set = 500
        expected_value = f"Pico toolbox confirms that the ADC capture depth is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_capture_depth, value_to_set)
        self.assertEqual(expected_value, real_value)

    def test_set_adc_sample_rate(self):
        global pico
        value_to_set = 50000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set))
        self.assertEqual(expected_value, real_value)

    def test_get_adc_capture_depth(self):
        global pico
        value_to_set = 500
        expected_value = f"Pico toolbox confirms that the ADC capture depth is set to: {value_to_set}"
        capture_depth = pico.set_setting(SettingsSelector.set_adc_capture_depth, value_to_set)
        self.assertEqual(expected_value, capture_depth, "Test init failed")
        expected_value = "500"
        real_value = pico.get_setting(SettingsSelector.get_adc_capture_depth)
        self.assertEqual(expected_value, real_value)

    def test_get_adc_sample_rate(self):
        global pico
        value_to_set_1 = 50000
        expected_value = f"Pico toolbox confirms that the ADC sample rate is set to: {value_to_set_1}"
        sample_rate = pico.set_setting(SettingsSelector.set_adc_sample_rate, pico._sample_rate_to_clock_devide(value_to_set_1))
        self.assertEqual(expected_value, sample_rate, "Test init failed")
        expected_value = 960
        real_value = pico.get_setting(SettingsSelector.get_adc_sample_rate)
        self.assertEqual(expected_value, real_value)

    def test_set_adc_amplification(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the ADC amplification is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_adc_amplification, value_to_set)
        self.assertEqual(expected_value, real_value)

    def test_set_channel_number(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the Channel number is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_channel_number, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_wave_type(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the AWG wave type is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_awg_wave_type, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_dac_freq(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the DAC freq is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_dac_freq, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_dac_channel_number(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the DAC channel number is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_dac_channel_number, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_peak_to_peak(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the Peak to Peak is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_peak_to_peak, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_offset(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the AWG offset is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_awg_offset, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_mSeconds_per_dev(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the mSeconds per dev is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_mSeconds_per_dev, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_trigger(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the Trigger is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_trigger, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_direction(self):
        global pico
        value_to_set = 1
        expected_value = f"Pico toolbox confirms that the Direction is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_direction, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_mVolt_per_DIV(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the mVolt per DIV is set to: {value_to_set} "
        real_value = pico.set_setting(SettingsSelector.set_mVolt_per_DIV, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_duty_cycle(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the dutycycle is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_awg_duty_cycle, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_phase(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the set_awg_phase is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_awg_phase, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_enable_a(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the set_awg_enable_a is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_awg_enable_a, value_to_set)
        self.assertEqual(expected_value, real_value)
    def test_set_awg_enable_b(self):
        global pico
        value_to_set = 5
        expected_value = f"Pico toolbox confirms that the set_awg_enable_b is set to: {value_to_set}"
        real_value = pico.set_setting(SettingsSelector.set_awg_enable_b, value_to_set)
        self.assertEqual(expected_value, real_value)