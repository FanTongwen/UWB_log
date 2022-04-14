import serial
import time
import numpy as np
from fileWriter import *
ser = serial.Serial(
    port="COM9",              # number of device, numbering starts at
    # zero. if everything fails, the user
    # can specify a device string, note
    # that this isn't portable anymore
    # if no port is specified an unconfigured
    # an closed serial port object is created
    baudrate=115200,          # baud rate
    bytesize=serial.EIGHTBITS,     # number of databits
    parity=serial.PARITY_NONE,     # enable parity checking
    stopbits=serial.STOPBITS_ONE,  # number of stopbits
    timeout=1,           # set a timeout value, None for waiting forever
    xonxoff=0,              # enable software flow control
    rtscts=0,               # enable RTS/CTS flow control
    interCharTimeout=None   # Inter-character timeout, None to disable
)

#ser.open()
if ser.is_open:
    print("open success")
else:
    print("open failed")

i = 0
j = 0
BaseStationNum = 4
d = [0 for col in range(BaseStationNum)]
file_uwbdata = fileWriter(r'.\data\file_uwbdata.txt')
while True:
    if ser.in_waiting:
        str1 = ser.read(ser.in_waiting).decode("gbk")
        if str1 == "exit":  # 退出标志
            break
        else:
            str1_1 = str1[0:64]
            str1_2 = str1[65:-1]
            tag = str1_1[0:2]
            # d_0 = str1_1[6:14]   # a0 到标签距离
            # d_1 = str1_1[15:23]  # a1 到标签距离
            # d_2 = str1_1[24:32]  # a2 到标签距离
            # d_3 = str1_1[33:41]  # a3 到标签距离
            if tag == "mc":
                for i in range(BaseStationNum):
                    d_hex = str1_1[6 + i*9: 14 + i*9]
                    d[i] = int(d_hex, 16)
                    d[i] = float(d[i]) / 1000.0
                file_uwbdata.file_handle.write("%.3f %6.3f %6.3f %6.3f %6.3f\n" %
                                               (time.time(), d[0], d[1], d[2], d[3]))
                file_uwbdata.file_handle.flush()
