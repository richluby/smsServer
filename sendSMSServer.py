#!/usr/bin/python

import sys, getopt, SocketServer
from objects import ThreadingUDPHandler, ThreadingUDPServer
from objects import Packet

#the configuration dictionary
_CONF_DICT = {}
# the port on which to listen
_CONF_DICT["port"] = 8658
# the IP to which to bind
_CONF_DICT["ip"] = "127.0.0.1"
# the configuration file to read
# most configuration files go in /etc on a Linux system
_CONF_DICT["confFile"] = "smsServer.conf"
# the number of seconds to keep a number in memory
# default is 1800 (30min)
_CONF_DICT["timeout"] = 1800
# determines if the server should fork a back ground process or not
_CONF_DICT["background"] = False
# the set of numbers known to the server at any given time
numberSet = set()

# reads the configuration file and populates the correct fields
def readConfiguration():
	lines = []
	global _CONF_DICT
	try:
		with open(_CONF_DICT["confFile"]) as f:
			lines = f.readlines()
	except IOError:
		print "ERROR: Failed to parse", _CONF_DICT["confFile"],". Proceeding with current configuration."
		return 0
	tokens = []
	for line in lines:
		tokens = line.split(" ")
		if (tokens[0] == "Timeout"):
			_CONF_DICT["timeout"] = int(tokens[1])
		elif (tokens[0] == "Port"):
			_CONF_DICT["port"] = int(tokens[1])
		elif (tokens[0] == "Background"):
			_CONF_DICT["background"] = bool(tokens[1])


# prints the help and then exits
def printHelp():
	print "\nOctober 2015 \n\
	Creates a server that sends SMS messages to specified phone numbers. \n\
	Default configuration file is in" , (_CONF_DICT["confFile"]), ".\n"
	print "	-h		prints this help, and then exits\n\
	-b		forks the server into the background\n\
	-p <number>	sets the port on which to listen\n\
	-c <file>	sets the configuration file\n\
	-t <seconds>	sets the timeout in seconds to keep a number in \n\
			memory. Default is", (_CONF_DICT["timeout"]), "."
	exit(0)

# parses the command line arguments
def parseArgs():
	args, opts = getopt.gnu_getopt(sys.argv[1:], "p:c:t:hb",[""])
	global _CONF_DICT
	for arg, opt in args:
		if (arg == "-h"):
			printHelp()
		elif (arg == "p"):
			_CONF_DICT["port"] = int(opt)
		elif (arg == "c"):
			_CONF_DICT["confFile"] = opt
		elif (arg == "t"):
			_CONF_DICT["timeout"] = int(opt)

# starts a server on PORT that listens for UDP packets
def setupServer():	
	server = ThreadingUDPServer((_CONF_DICT["ip"], _CONF_DICT["port"]), ThreadingUDPHandler)
	return server

if __name__ == "__main__":
	parseArgs()	
	readConfiguration()
	server = setupServer()
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		server.close()
