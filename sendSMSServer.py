#!/usr/bin/python

import sys, getopt

# the port on which to listen
PORT = 8656
# the configuration file to read
# most configuration files go in /etc on a Linux system
CONF_FILE = "smsServer.conf"
# the number of seconds to keep a number in memory
# default is 1800 (30min)
TIMEOUT = 1800
# determines if the server should fork a back ground process or not
BACKGROUND = False

# reads the configuration file and populates the correct fields
def readConfiguration():
	lines = []
	try:
		with open(CONF_FILE) as f:
			lines = f.readlines()
	except IOError:
		print "ERROR: Failed to parse", CONF_FILE,". Proceeding with current configuration."
		return 0
	print lines

# prints the help and then exits
def printHelp():
	print "\nOctober 2015 \n\
	Creates a server that sends SMS messages to specified phone numbers. \n\
	Default configuration file is in" , (CONF_FILE), ".\n"
	print "	-h		prints this help, and then exits\n\
	-b		forks the server into the background\n\
	-p <number>	sets the port on which to listen\n\
	-c <file>	sets the configuration file\n\
	-t <seconds>	sets the timeout in seconds to keep a number in \n\
			memory. Default is", (TIMEOUT), "."
	exit(0)

# parses the command line arguments
def parseArgs():
	args, opts = getopt.gnu_getopt(sys.argv[1:], "p:c:t:h",[""])
	for arg, opt in args:
		if (arg == "-h"):
			printHelp()
		elif (arg == "p"):
			PORT = int(opt)
		elif (arg == "c"):
			CONF_FILE = opt
		elif (arg == "t"):
			TIMEOUT = int(opt)

if __name__ == "__main__":
	parseArgs()	
	print "Starting SMS Server..."
	readConfiguration()
