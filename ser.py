import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
    
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

ser = serial.Serial("COM5", 9600)

while True:
    data = (ser.readline())
    string = str(data, 'UTF-8')
    print(string)
    time.sleep(1)