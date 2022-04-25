import time
import numpy as np
from fileWriter import *
import rospy
from std_msgs.msg import String
import serial

rospy.init_node('uwb')

ser = serial.Serial(
    port="/dev/ttyACM0",              
    baudrate=115200,          # baud rate
    bytesize=serial.EIGHTBITS,     # number of databits
    parity=serial.PARITY_NONE,     # enable parity checking
    stopbits=serial.STOPBITS_ONE,  # number of stopbits
    timeout=1,           # set a timeout value, None for waiting forever
    xonxoff=0,              # enable software flow control
    rtscts=0,               # enable RTS/CTS flow control
    interCharTimeout=None   # Inter-character timeout, None to disable
)

# ser.open()
if ser.is_open:
    print("open success")
else:
    print("open failed")

i = 0
j = 0
BaseStationNum = 4

d = [0 for col in range(BaseStationNum)]
file_uwbdata = fileWriter(r'./data/file_uwbdata.txt')
while True:
    if ser.in_waiting:
        timestamp = rospy.Time.now()
        str1 = ser.read(ser.in_waiting).decode("gbk")
        if str1 == "exit": 
            break
        else:
            str1_1 = str1[0:64]
            str1_2 = str1[65:-1]
            tag = str1_1[0:2]
            #print(timestamp.to_sec())

            if tag == "mc" and len(str1_1) == 64:
                for i in range(BaseStationNum):
                    d_hex = str1_1[6 + i*9: 14 + i*9]
                    d[i] = int(d_hex, 16)
                    d[i] = float(d[i]) / 1000.0
                print("%.5f %6.3f %6.3f %6.3f %6.3f\n" %
                                               (timestamp.to_sec(), d[0], d[1], d[2], d[3]))
                file_uwbdata.file_handle.write("%.5f %6.3f %6.3f %6.3f %6.3f\n" %
                                               (timestamp.to_sec(), d[0], d[1], d[2], d[3]))
                file_uwbdata.file_handle.flush()
