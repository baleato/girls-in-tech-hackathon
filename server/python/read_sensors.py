import serial

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

	temperature = get_temperature(ser)
	humidity = get_humidity(ser)
	air_quality = get_air_quality(ser)
	timestamp = get_timestamp()
	value = str(timestamp) + " " + str(humidity) + " " + str(temperature) + " " + str(air_quality) + "\n"
	write_to_file("Sensordata.txt",value)
	print value


	ser.flush()
	ser.close()
except:
	ser.flush()
	ser.close()
	raise