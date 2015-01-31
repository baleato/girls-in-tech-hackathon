# -*- coding: utf-8 -*-
"""
Created on Wed Jan 07 12:59:20 2015

@author: Peter Bremer, Philips Consumer Lifestyle, Drachten
"""

import serial
import time

from clcpbt import send_packet_param
from clcpbt import send_packet
from clcpbt import read_packet
from clcpbt import lo_hi_byte
#from clcpbt import get_value_data_packet
#from clcpbt import get_4values_datapacket
#from clcpbt import decode_packet

# ------------------------------------------------------------------------
ser = serial.Serial(port='/dev/tty.WUL-DevB',
                    baudrate=9600,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=None,
                    xonxoff=0,
                    rtscts=0)

try:
    if not ser.isOpen():
        ser.open()


    print "=================================================="
    print "Turning light off..."

    send_packet_param(ser, 0x06, 0x0006, [0x04])


    print "=================================================="



    ser.flush()
    ser.close()
except:
    ser.flush()
    ser.close()
    raise

