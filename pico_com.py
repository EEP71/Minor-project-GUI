import serial
import time
import threading
from enum import Enum
import numpy as np

class ToolSelector(Enum):
    """
    Tool selector enum for selecting the tools
    """
    AWG = b'1' # Arbitrary waveform generator 
    LIA = b'2' # Lock-in amplifier
    SA = b'3'  # Spectrum analyser
    scope = b'4' # Oscilloscope
    AWG_and_scope = b'5' # Arbitrary waveform generator and Oscilloscope
    AWG_and_LIA = b'6' # Arbitrary waveform generator and Lock-in amplifier
    AWG_and_SA = b'7' # Arbitrary waveform generator and Spectrum analyser
    change_settings = b'8' # Change toolbox settings
    toolbox_values = b'9' # Get values from toolbox
    no_tool = b'0' # Terminate program

class SettingsSelector(Enum):
    """
    Settings selector enum for selecting the settings
    """
    set_adc_capture_depth   = b'a'
    set_adc_sample_rate     = b'b'
    set_adc_amplification   = b'c'
    set_channel_number      = b'd'

    set_awg_wave_type       = b'e'
    set_dac_freq            = b'f'
    set_dac_channel_number  = b'g'
    set_peak_to_peak        = b'h'
    set_awg_offset          = b'i'

    set_mSeconds_per_dev    = b'j'
    set_trigger             = b'k'
    set_direction           = b'l'
    set_mVolt_per_DIV       = b'm'

    get_adc_capture_depth   = b'n'
    get_adc_sample_rate     = b'o'
    set_awg_duty_cycle      = b'p'
    set_awg_phase           = b'q'
    set_awg_enable_a        = b'r'
    set_awg_enable_b        = b's'

class PicoCom:

    """
    A class used to communicate with the Pico toolbox. Don't use the attributes to change stuff use the methods instead!

    ...

    Attributes
    ----------
    SA_values : np.ndarray of np.float32
        ndarray of values from the spectrum analyser
    scope_values : np.ndarray of np.float32
        ndarray of values from the oscilloscope
    communication_speed_hz : int
        Communication speed in Hz (default 10)
    serial_com : serial.Serial()
        Serial communication class, never change this!!
    SA_thread_event : threading.Event()
        Spectrum analyser threading event, never change this!!
    LIA_thread_event : threading.Event()
        LIA threading event, never change this!!
    scope_thread_event : threading.Event()
        Oscilloscope threading event, never change this!!
    AWG_thread_event : threading.Event()
        AWG threading event, never change this!!
    tool_select : ToolSelector
        Current selected tool, never change this!!


    """
    def __init__(self, com: str):
        """
        ...

        Parameters
        ----------
        com : str
            Serial communication port to use for the Pico toolbox
        """
        self.serial_com      = serial.Serial(com)
        self.SA_thread_event = threading.Event()
        self.LIA_thread_event = threading.Event()
        self.scope_thread_event = threading.Event()
        self.tool_select =  ToolSelector.no_tool
        self.SA_values =    np.empty([0, 0], dtype=np.float32)
        self.scope_values = np.empty([0, 0], dtype=np.float32)
        self.communication_speed_hz = 10 #Reading speed in HZ from the pi pico 10hz works for sure
        self.capture_depth = 1
        self._init_pico_threads()

    def _init_pico_threads(self):
        """ Initialize communication threads"""

        SA_thread        = threading.Thread(target=self._SA_thread, args=(self.SA_thread_event,))
        SA_thread.name   = "FFT_thread"
        SA_thread.daemon = True
        self.SA_thread_event.clear()
        SA_thread.start()

        LIA_thread        = threading.Thread(target=self._lia_thread, args=(self.LIA_thread_event,))
        LIA_thread.name   = "LIA_thread"
        LIA_thread.daemon = True
        self.LIA_thread_event.clear()
        LIA_thread.start()

        scope_thread        = threading.Thread(target=self._scope_thread, args=(self.scope_thread_event,))
        scope_thread.name   = "scope_thread"
        scope_thread.daemon = True
        self.LIA_thread_event.clear()
        scope_thread.start()

    def _select_command(self, selector):
        """Selects the command from set_tool()
        1: Arbitrary waveform generator
        2: Lock-in amplifier
        3: Spectrum analyser
        4: Oscilloscope
        5: Arbitrary waveform generator and Oscilloscope
        6: Arbitrary waveform generator and Lock-in amplifier
        7: Arbitrary waveform generator and Spectrum analyser
        8: Change toolbox settings
        9: Get values from toolbox
        """
        if self.tool_select == ToolSelector.no_tool:
            self._stop_all_threads()
            self._send_data_to_pico(ToolSelector.no_tool.value)
            self.tool_select = 0
        elif self.tool_select == ToolSelector.AWG:
            self._stop_all_threads()
            self._send_data_to_pico(ToolSelector.AWG.value)
            self.tool_select = 0
        elif self.tool_select == ToolSelector.LIA:
            self._stop_all_threads()
            self.LIA_thread_event.set()
            self.tool_select = 0
        elif self.tool_select == ToolSelector.SA:
            self._stop_all_threads()
            self.SA_thread_event.set()
            self.tool_select = 0
        elif self.tool_select == ToolSelector.scope:
            self._stop_all_threads()
            self.scope_thread_event.set()
            self.tool_select = 0
        elif self.tool_select == ToolSelector.AWG_and_scope:
            self._stop_all_threads()
            self._send_data_to_pico(ToolSelector.AWG_and_scope.value)
            self.tool_select = 0
        elif self.tool_select == ToolSelector.AWG_and_LIA:
            self._stop_all_threads()
            print("AWG_and_LIA")
            self.tool_select = 0
        elif self.tool_select == ToolSelector.AWG_and_SA:
            self._stop_all_threads()
            self._send_data_to_pico(ToolSelector.AWG_and_SA.value)
            self.tool_select = 0
        elif self.tool_select == ToolSelector.change_settings:
            self._stop_all_threads()
            self.tool_select = 0
        elif self.tool_select == ToolSelector.toolbox_values:
            self._stop_all_threads()
            self.tool_select = 0
        else:
            pass

    def set_setting(self, setting: SettingsSelector, value: int) -> str:
        """
        Sets the given value to the given setting on the Pico Toolbox
        ...
        Parameters
        ----------
        setting : SettingsSelector
            The setting which needs to be changed
        value : int
            The value that the setting will be set to
        """
        self.set_tool(ToolSelector.change_settings)
        self._send_data_to_pico(ToolSelector.change_settings.value)
        self._send_data_to_pico(setting.value)
        if setting == SettingsSelector.set_adc_sample_rate:
            value = self._sample_rate_to_clock_devide(value)
        self._send_data_to_pico((str(value) + '\n' ).encode())
        time.sleep(0.1)
        try:
            return self._get_data_from_pico().decode()
        except:
            return self._get_data_from_pico()


    def get_setting(self, setting: SettingsSelector) -> str:
        """
        Sets the given value to the given setting on the Pico Toolbox

        ...

        Parameters
        ----------
        setting : SettingsSelector
            The setting you want to receive
        """
        self.set_tool(ToolSelector.change_settings)
        self._send_data_to_pico(ToolSelector.change_settings.value)
        self._send_data_to_pico(setting.value)
        time.sleep(0.1)
        try:
            if setting == SettingsSelector.get_adc_sample_rate:
                value = self._get_data_from_pico().decode()
                value = self._clock_devide_to_sample_rate(value)
                return value
            else:
                return self._get_data_from_pico().decode()
        except:
            if setting == SettingsSelector.set_adc_sample_rate:
                value = str(self._get_data_from_pico())
                value = self._clock_devide_to_sample_rate(value)
                return value
            else:
                return self._get_data_from_pico()


    def set_tool(self, tool: ToolSelector):
        """
        Sets the given tool on the Pico Toolbox

        ...

        Parameters
        ----------
        tool : ToolSelector 
            The setting which needs to be changed
        """
        self.tool_select = tool
        self._select_command(self.tool_select)

    def get_SA_values(self) -> np.ndarray:
        """
        Returns the latest spectrum analyser values

        ...

        Returns
        ----------
        SA_values : np.ndarray of np.float32
            The latest spectrum analyser values from the Pico toolbox
        """
        return self.SA_values

    def get_scope_values(self) -> np.ndarray:
        """
        Returns the latest oscilloscope values

        ...

        Returns
        ----------
        scope_values : np.ndarray of np.float32
            The latest oscilloscope values from the Pico toolbox
        """
        return self.scope_values

    def _send_data_to_pico(self, data):
        "Sends data to the pico Toolbox buffer"
        self.serial_com.write(data)

    def _get_data_from_pico(self):
        "Reads data buffer from the Pico toolbox"
        data_str = 0
        while (self.serial_com.in_waiting > 0):
            data_str = self.serial_com.read(self.serial_com.in_waiting)
        return data_str

    def _SA_thread(self, e):
        "SA thread that gets the SA values from the Pico toolbox and converts data to numpy array"
        while True:
            e.wait()
            self._send_data_to_pico(ToolSelector.SA.value)
            time.sleep(1/self.communication_speed_hz)
            raw_data = self._get_data_from_pico()
            try:
                if (raw_data != 0):
                    decoded_data = raw_data.decode()
                    mapped_data = map(float, decoded_data.rstrip("\n").rstrip("\r").split(",")[:-1])
                    SA_values_array = np.fromiter(mapped_data, dtype=np.float32)
                    SA_log_scale = np.log10(np.sqrt(SA_values_array) / self.capture_depth) * 10
                    highest_value = np.amax(SA_log_scale)
                    lowest_value = np.amin(SA_log_scale)
                    self.SA_values = SA_log_scale
            except:
                print("SOrry zal dit fixe")


    def set_capture_depth(self, capture_depth: int):
        """
        Sets capture depth, important for spectrum analyzer fft plot set this for a better plot

        ...

        Parameters
        ----------
        capture_depth : int  
            The capture depth to change after chaning capture depth in settings.
        """
        self.capture_depth = capture_depth
    def _lia_thread(self, e):
        "LIA thread"
        while True:
            e.wait()
            print("LIA THREAD RUNNING")

    def _scope_thread(self, e):
        "Scope thread that gets the scope values from the Pico toolbox and converts data to numpy array"
        while True:
            e.wait()
            self._send_data_to_pico(ToolSelector.scope.value)
            time.sleep(1/self.communication_speed_hz)
            raw_data = self._get_data_from_pico()
            try:
                if (raw_data != 0):
                    decoded_data = raw_data.decode()
                    mapped_data = map(int, decoded_data.rstrip("  ").rstrip("\r").split(",")[:-1])
                    self.scope_values = np.fromiter(mapped_data, dtype=int)
            except:
                print("SOrry zal dit fixe")

    def _stop_all_threads(self):
        "pauses all running threads"
        self.SA_thread_event.clear()
        self.LIA_thread_event.clear()
        self.scope_thread_event.clear()
        # self.serial_com.cancel_read()
        # self.serial_com.cancel_write()
        # # self.serial_com.reset_input_buffer()
        # # self.serial_com.reset_output_buffer()
        # # self.serial_com.flush()
        # # self.serial_com.flushInput()
        # # self.serial_com.flushOutput()

    def _select_settings(self, setting_selector):
        """
        TODO
        """
        pass


    def _sample_rate_to_clock_devide(self, sample_rate):
        clock_devide_value = 48000000//int(sample_rate)
        return clock_devide_value


    def _clock_devide_to_sample_rate(self, clock_devide):
        sample_rate_value = 48000000//int(clock_devide)
        return sample_rate_value