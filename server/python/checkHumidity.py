import serial
import time

#import sensormethods
from sensormethods import get_timestamp
from sensormethods import get_temperature
from sensormethods import get_humidity
from sensormethods import get_air_quality
from sensormethods import write_to_file
from sensormethods import get_mains_on_off

# ------------------------------------------------------------------------
ser = serial.Serial(port='/dev/tty.STYLER-DevB',
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

    print get_humidity(ser)

    ser.flush()
    ser.close()

except:
    ser.flush()
    ser.close()
    raise