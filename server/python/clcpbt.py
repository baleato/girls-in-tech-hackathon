# -*- coding: utf-8 -*-
"""
Communicates data packages via a serial communictation interface.

1) Sending and reading complete packages:
send_packet:
    Sends a complete package via a serial communication line.

send_packet_param:
    Sends a package for port 0xD003 as defined in the protocol.

read_packet(ser):
    Reads a complete package and returns it.

2) Decoding packages
decode_packet:
    Decodes the package in 'buff' and prints all its information.

3) Reading values
get_value_data_packet(buff):
    Get a one or two byte value from a package in buff.

get_4values_datapacket(buff):
    Get a four times two byte value from a package in buff.

get_struct_values_data_packet(partial_buff):
    Get a sequence of values from partial_buff.

-----------------------------------------------------------------
Created on Tue Jan 20 08:04:29 2015
@author: Peter Bremer, Philips Consumer Lifestyle, Drachten
"""

# General support functions

def lo_hi_byte(num):
    """" Splits a word in Low byte and High byte."""
    return (num & 0xFF), (num >> 8)

def write_word(ser, word):
    """ Writes a word to the serial line."""
    low, high = lo_hi_byte(word)
    ser.write(chr(low))
    ser.write(chr(high))

def write_byte(ser, byt):
    """ Writes a byte to the serial line."""
    ser.write(chr(byt))

def read_word(buff, low, high):
    """ Reads a word from the buffer at index low and high."""
    return ord(buff[low]) + 256 * ord(buff[high])

def read_byte(buff, index):
    """ Reads a byte from the buffer at index."""
    return ord(buff[index])


# 1) Sendng and reading complete packages

def send_packet(ser, port, cmd, payload): # payload is a list of byte values
    """
    Sends a complete package via a serial communication line.

    It adds the starting and closing sequences.
    ser:        serial communicatioon line
    port:       port as defined in the protocol
    cmd:        command as defined in the protocol
    payload:    the rest of the information accoring the protocol

    """

    addr_source = 0x0000
    addr_destination = 0x0001

    ser.write("[/--->/]")

    write_word(ser, addr_source)
    write_word(ser, addr_destination)
    write_word(ser, port)                # source port
    write_word(ser, port)                # destination port
    write_word(ser, 1 + len(payload))    # len
    write_word(ser, 0x0000)              # checksum, not used yet
    write_byte(ser, cmd)
    for character in payload:
        write_byte(ser, character)

    ser.write("[/<---/]")

def send_packet_param(ser, cmd, param, payload):
    """
    Sends a package for port 0xD003 as defined in the protocol.

    ser:        serial communicatioon line
    cmd:        command as defined in the protocol
    param:      parameter number as defined in the protocol
    payload:    the rest of the information accoring the protocol
    """

    low, high = lo_hi_byte(param)
    newpayload = [low, high]
    newpayload.extend(payload)
    send_packet(ser, 0xD003, cmd, newpayload)

def read_packet(ser):
    """
    Reads a complete package and returns it.
    """

    buff = ''
    while buff[-8:] != "[/<---/]":
        while ser.inWaiting() > 0:
            character = ser.read()
            buff += character
    return buff


# 2) Decoding of packages
def decode_packet(buff):
    """
    Decodes the package in 'buff' and prints all its information.
    """

    packet_addr_source = read_word(buff, 8, 9)
    print "Source addess: 0x{:04x}".format(packet_addr_source)
    packet_addr_destination = read_word(buff, 10, 11)
    print "Destination address: 0x{:04x}".format(packet_addr_destination)

    packet_port_source = read_word(buff, 12, 13)
    print "Source port: 0x{:04x}".format(packet_port_source)
    packet_port_destination = read_word(buff, 14, 15)
    print "Destination port: 0x{:04x}".format(packet_port_destination)

    packet_len = read_word(buff, 16, 17)
    print "Length: 0x{:04x}".format(packet_len)
    packet_checksum = read_word(buff, 18, 19)
    print "Checksum: 0x{:04x}".format(packet_checksum)

    packet_command = read_byte(buff, 20)
    print "Command: 0x{:02x}".format(packet_command)

    packet_payload = ''
    if len(buff) > 20:
        packet_payload = buff[20:-8]

    print "Payload:"
    print "-------------------------------------------------------------------"
    print "1) In hex"
    print ":".join("{:02x}".format(ord(c)) for c in packet_payload)
    print "-------------------------------------------------------------------"
    print "2) As characters with : seperator"
    buff = ''
    for character in packet_payload:
        if ord(character) >= 0x20 and ord(character) < 127:
            buff += character + ':'
        else:
            buff += "0x{0:02x}:".format(ord(character))
    print buff
    print "-------------------------------------------------------------------"
    print "3) As character/hex with : seperator"
    buff = ''
    for character in packet_payload:
        if ord(character) >= 0x20 and ord(character) < 127:
            buff += "'{0}'/0x{1:02x}:".format(character, ord(character))
        else:
            buff += "0x{0:02x}:".format(ord(character))
    print buff

#  3) Reading values
def get_value_data_packet(buff):
    """ Get a one or two byte value from a package in buff."""
    if len(buff) > 25:
        nbytes = ord(buff[24])
        if nbytes == 1:
            return ord(buff[25])
        elif nbytes == 2:
            return ord(buff[25])+256*ord(buff[26])
        else:
            return ''
    else:
        return ''

def get_4values_datapacket(buff):
    """ Get a four times two byte value from a package in buff."""
    if len(buff) > 34:
        nbytes = ord(buff[24])
        if nbytes == 8:
            return  ord(buff[25])+256*ord(buff[26]), \
                    ord(buff[27])+256*ord(buff[28]), \
                    ord(buff[29])+256*ord(buff[30]), \
                    ord(buff[31])+256*ord(buff[32])
        else: return ''
    else:
        return ''

def get_struct_values_data_packet(partial_buff):
    """ Get a sequence of values from buff """
    vals = []
    itbuff = iter(partial_buff)

    while True:
        try:
            nbytes = ord(itbuff.next())
            if nbytes == 1:
                val = ord(itbuff.next())
                vals.append(val)
            elif nbytes == 2:
                val = ord(itbuff.next()) + 256 * ord(itbuff.next())
                vals.append(val)
            elif nbytes == 8:
                #pylint: disable=W0612
                for i in range(0, 4):
                    val = ord(itbuff.next()) + 256 * ord(itbuff.next())
                    vals.append(val)
        except StopIteration:
            break
    return vals





#print "packet received"
#decode_packet(buff)

#print "packet received"
#decode_packet(buff)
