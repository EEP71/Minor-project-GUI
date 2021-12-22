import serial
import time
import sys
import threading

class PicoCom:
    def __init__(self, com):
        self.serial_com      = serial.Serial(com)
        self.fft_values      = 0
        self.samples         = 0
        self.sample_rate     = 50000 # Sample rate in Hz
        self.capture_depth   = 1000  # Quantity of samples
        self.base_clock      = 48000000
        self.adc_bit         = 12
        self.fft_thread_event = threading.Event()
        self.sample_thread_event = threading.Event()

    def init_pico_threads(self):
        """ Init threads for plotting, call this function once and before plotting"""
        main_thread     = threading.Thread(target=self._select_command, args=())
        fft_thread      = threading.Thread(target=self._fft_thread, args=(self.fft_thread_event,))
        sample_thread   = threading.Thread(target=self._sample_thread, args=(self.sample_thread_event,))
        main_thread.name = "Pico_main_thread"
        fft_thread.name = "FFT_thread"
        sample_thread.name = "Sample_thread"
        fft_thread.daemon = True
        main_thread.daemon = True
        sample_thread.daemon = True
        self.fft_thread_event.clear()
        self.sample_thread_event.clear()
        main_thread.start()
        fft_thread.start()
        sample_thread.start()

    def _select_command(self):

        """Select the command from user input BLOCKING!!!!
        0: Stop sample plots
        1: FFT
        2: Samples
        3: Sample rate
        4: usb test
        5: Change capture depth
        6: Change clock_divide
        7: fft plot
        8: sample plot
        9: Stop Program
        """
        while True:
            user_input = input("\n\n\n0: Stop sample plots\n1: FFT\n2: Samples\n3: Sample rate\n4: usb test\n5: Change capture depth\n6: Change sample rate\n7: FFT plot\n8: Sample plot\n9: Stop Program\n").encode()
            if user_input == b'0':
                if self._check_if_thread_is_running():
                    self.fft_thread_event.clear()
                    self.sample_thread_event.clear()
                else:
                    print("There is no active plot")
            elif user_input == b'1':
                if self.fft_thread_event.is_set():
                    self._print_fft()
                else:
                    self._get_fft_values(user_input)
                    self._print_fft()
            elif user_input == b'2':
                if self.sample_thread_event.is_set():
                    self._print_samples()
                else:
                    self._get_samples(user_input)
                    self._print_samples()
            elif user_input == b'3':
                #Sample rate
                if self._check_if_thread_is_running():
                    print(f"Sample rate: {self.sample_rate} Hz")
                else:
                    self._get_sample_rate(user_input)
                    print(f"Sample rate: {self.sample_rate} Hz")
            elif user_input == b'4':
                if self._check_if_thread_is_running():
                    print("Plot is running can't do USB speed test")
                else:
                    self._usb_speed_test(user_input)
            elif user_input == b'5':
                #Change capture depth
                if self._check_if_thread_is_running():
                    print("Plot is running so capture depth can't be changed")
                else:
                    self._change_capture_depth(user_input)
            elif user_input == b'6':
                #Change sample rate
                if self._check_if_thread_is_running():
                    print("Plot is running so sample rate can't be changed")
                else:
                    self._change_sample_rate(user_input)
                pass
            elif user_input == b'7':
                #FFT thread
                self.sample_thread_event.clear()
                self.fft_thread_event.set()

            elif user_input == b'8':
                #sample thread
                self.fft_thread_event.clear()
                self.sample_thread_event.set()

            elif user_input == b'9':
                quit()

    def _send_data_to_pico(self, user_input):
        """Sends data input to pico when not expecting something back.
        Keyword arguments:
        input -- Data to send to pico must be a byte string
        """
        self.serial_com.write(user_input)

    def _send_get_data_from_pico(self, user_input):
        """ Sends data input to pico returns data from Pico.
            ONLY USE THIS WHEN EXPECTING AN ANWSNER FROM THE PICO OR ELSE......
        Keyword arguments:
        input -- Data to send to pico must be a byte string
        """
        self.serial_com.write(user_input)
        return self.serial_com.readline().decode()

    def _get_data_from_pico(self):
        """ Returns data from Pico.
            ONLY USE THIS WHEN EXPECTING AN ANWSNER FROM THE PICO OR ELSE......
        """
        return self.serial_com.readline().decode()

    def _get_fft_values(self, user_input):
        self.fft_values = self._send_get_data_from_pico(user_input)

    def _get_samples(self, user_input):
        self.samples = self._send_get_data_from_pico(user_input)

    def _get_sample_rate(self, user_input):
        self._send_get_data_from_pico(user_input)
        data = self._get_data_from_pico()
        self.sample_rate = self._get_numbers_from_string(data)[:-1]

    def _usb_speed_test(self, user_input):
        print("The speedtest will take about 10 seconds be patient")
        self._send_data_to_pico(user_input)

        start_time = time.time()
        speedtest_data = self._get_data_from_pico()
        end_time = time.time()

        size_bytes_received = sys.getsizeof(speedtest_data)
        time_to_receive = end_time - start_time
        time_formatted = "{:.2f}".format(time_to_receive)
        print (f"My program took {time_formatted} seconds to receive {size_bytes_received} bytes")
        bytes_per_second = int(size_bytes_received / time_to_receive)
        print (f" {bytes_per_second} Bytes/s")
        bits_received = size_bytes_received * 8
        bits_per_second = int(bits_received / time_to_receive)
        print (f" {bits_per_second} Bits/s")
        mBits_received = size_bytes_received / 125000
        mBits_per_second = mBits_received / time_to_receive
        mBits_per_second_formatted = "{:.2f}".format(mBits_per_second)
        print (f" {mBits_per_second_formatted} mBits/s")

    def _change_capture_depth(self, user_input):
        user_input2 = input(f"\n\nEnter capture depth, current value: {self.capture_depth}\n")
        self._send_data_to_pico(user_input)
        data =  self._send_get_data_from_pico((user_input2 + '\n').encode())
        self.capture_depth = self._get_numbers_from_string(data)

    def _change_sample_rate(self, user_input):
        user_input2 = input(f"\n\nEnter sample rate, current value: {self.sample_rate} Hz\n")
        clock_devide_value = str(self.base_clock/int(user_input2))
        self._send_data_to_pico(user_input)
        data =  self._send_get_data_from_pico((clock_devide_value + '\n').encode())
        temp_clock_devide = self._get_numbers_from_string(data)[:-1]
        self.sample_rate = self.base_clock // int(temp_clock_devide)

    def _get_numbers_from_string(self, string):
        number_string = filter(str.isdigit, string)
        return "".join(number_string)

    def _print_samples(self):
        print(self.samples)

    def _print_fft(self):
        print(self.fft_values)

    def _fft_thread(self, e):
        while True:
            e.wait()
            self.fft_values = self._send_get_data_from_pico(b'1')

    def _sample_thread(self, e):
        while True:
            e.wait()
            self.samples = self._send_get_data_from_pico(b'2')


    def _check_if_thread_is_running(self):
        if self.fft_thread_event.is_set() or self.sample_thread_event.is_set():
            return True
        else:
            return False

if __name__ == "__main__":
    pico = PicoCom("/dev/")
    pico.init_pico_threads()