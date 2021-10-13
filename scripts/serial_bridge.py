#!/usr/bin/python3
#
# Receives UDP multicast datagrams as broadcast by a Microhard radio
# in UDP Point to Multipoint(P) mode, and forwards them to a selected
# serial port, optionally also printing them to stdout.
#

import sys
import serial
from optparse import OptionParser

import socket
import struct

parser = OptionParser(usage="usage: %prog [/dev/tty] [options]")
parser.add_option("-g", "--group", dest="group",
                  help="multicast IP", metavar="IP", default="224.1.1.1")
parser.add_option("-p", "--port", dest="port",
                  help="multicast port", metavar="PORT", default=20001)
parser.add_option("-d", "--device", dest="device",
                  help="multicast device", metavar="ETH", default="eth0")
parser.add_option("-b", "--baud", dest="baud",
                  help="serial baud rate", metavar="RATE", default=57600)
parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="echo received messages to stdout")

(options, args) = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((options.group, options.port))
mreq = struct.pack("4sl", socket.inet_aton(options.group), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Created UDP socket receiver.")

ser = None
ser_name = None
if len(args) >= 1:
  ser_name = args[0]

try:
  while True:
    s = sock.recv(10240)
    if ser_name and not ser:
      try:
        ser = serial.Serial(port=ser_name, baudrate=options.baud, timeout=0)
        print("Opened serial port.")
      except Exception as e:
        ser = None
        print(str(e))
    if ser:
      ser.write(s)
      ser.flush()
    if options.verbose:
      sys.stdout.write(str(s).encode("string_escape"))
      sys.stdout.flush()

except:
  if ser:
    ser.close()
    print("Closed serial port.")
  raise
