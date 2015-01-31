# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 10:57:23 2015

@author: Peter Bremer, Philips Consumer Lifestyle, Drachten
"""

import time

from clcpbt import send_packet_param
#from clcpbt import send_packet
from clcpbt import read_packet
#from clcpbt import lo_hi_byte
from clcpbt import get_value_data_packet
#from clcpbt import get_4values_datapacket
#from clcpbt import decode_packet
#from clcpbt import lo_hi_byte
from clcpbt import get_struct_values_data_packet

 # Returns the elapsed number of seconds since the epoch in UTC.
 # @return the elapsed number of seconds since the epoch in UTC.
 #
def get_timestamp():
	return time.time()

 # Returns the Philips sensor box temperature sensor value in celcius.
 # @param ser the serial object
 # @return the Philips sensor box temperature sensor value in celcius.
def get_temperature(ser):
	# Get the temperature value 
	send_packet_param(ser, 0x06, 0x000C, [0x00]) 
	buff = read_packet(ser)
	temperature = get_value_data_packet(buff)
	# Convert to celsius and return
	return ((temperature-100)/10.0)

 # Returns the Philips sensor box humidity sensor value as a percentage.
 # @param ser the serial object
 # @return the Philips sensor box humidity sensor value as a percentage.
def get_humidity(ser):
	# Get the humidity value
	send_packet_param(ser, 0x06, 0x000D, [0x00])
	buff = read_packet(ser)
	humidity = get_value_data_packet(buff)
	# Convert to a percentage and return it
	return humidity*10.0

 # Returns the Philips sensor box air quality sensor value in ppm
 # (parts per million).
 # @param ser the serial object
 # @return the Philips sensor box air quality sensor value in ppm
 #         (parts per million).
def get_air_quality(ser):
	# Get the air quality value
	send_packet_param(ser, 0x06, 0x000F, [0x00]) 
	buff = read_packet(ser)
	air_quality = get_value_data_packet(buff) 
	return air_quality


 # Returns an indication of whether the styler is turned on or off.
 # @param ser the serial object
 # @return the Philips sensor box air quality sensor value in ppm
 #         (parts per million).
def get_mains_on_off(ser):
	# Get the on/off indication
	send_packet_param(ser, 0x06, 0x001F, [0x00]) # mains on/off
	buff = read_packet(ser)
	mainstatus = get_value_data_packet(buff) 
	return mainstatus

 # Writes the timestamp, temperature, humidity and air quality values
 # to the sensor values file.
 # @param filename the name of the file to write to.
 # @param value the value to write to the file.
def write_to_file(filename, value):
	# Open the file
	file_pointer = open(filename, "w")
	# Write the values to the file
	file_pointer.write(value)
	# Close the file
	file_pointer.close()