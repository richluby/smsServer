#!/usr/bin/python

import sys, getopt, SocketServer
from ThreadingUDPServer import ThreadingUDPHandler, ThreadingUDPServer
from Packet import *

# the port on which to listen
_PORT = 8658
# the configuration file to read
# most configuration files go in /etc on a Linux system
_CONF_FILE = "smsServer.conf"
# the number of seconds to keep a number in memory
# default is 1800 (30min)
_TIMEOUT = 1800
# determines if the server should fork a back ground process or not
_BACKGROUND = False
# the set of numbers known to the server at any given time
numberSet = set()

# reads the configuration file and populates the correct fields
def readConfiguration():
	lines = []
	global _PORT
	global _TIMEOUT
	global _BACKGROUND
	try:
		with open(_CONF_FILE) as f:
			lines = f.readlines()
	except IOError:
		print "ERROR: Failed to parse", _CONF_FILE,". Proceeding with current configuration."
		return 0
	tokens = []
	for line in lines:
		tokens = line.split(" ")
		if (tokens[0] == "Timeout"):
			_TIMEOUT = int(tokens[1])
		elif (tokens[0] == "Port"):
			_PORT = int(tokens[1])
		elif (tokens[0] == "Background"):
			_BACKGROUND = bool(tokens[1])


# prints the help and then exits
def printHelp():
	print "\nOctober 2015 \n\
	Creates a server that sends SMS messages to specified phone numbers. \n\
	Default configuration file is in" , (_CONF_FILE), ".\n"
	print "	-h		prints this help, and then exits\n\
	-b		forks the server into the background\n\
	-p <number>	sets the port on which to listen\n\
	-c <file>	sets the configuration file\n\
	-t <seconds>	sets the timeout in seconds to keep a number in \n\
			memory. Default is", (_TIMEOUT), "."
	exit(0)

# parses the command line arguments
def parseArgs():
	args, opts = getopt.gnu_getopt(sys.argv[1:], "p:c:t:hb",[""])
	global _PORT
	global _TIMEOUT
	global _BACKGROUND
	for arg, opt in args:
		if (arg == "-h"):
			printHelp()
		elif (arg == "p"):
			_PORT = int(opt)
		elif (arg == "c"):
			_CONF_FILE = opt
		elif (arg == "t"):
			_TIMEOUT = int(opt)

# starts a server on PORT that listens for UDP packets
def setupServer():	
	server = ThreadingUDPServer(("127.0.0.1", _PORT), ThreadingUDPHandler)
	server.serve_forever()

if __name__ == "__main__":
	parseArgs()	
	readConfiguration()
	print "Starting SMS Server on port", _PORT,"..."
	setupServer()
