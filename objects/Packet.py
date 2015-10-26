#!/usr/bin/python

import struct

#contains the mapping of options to bit placement
_BITMAP = {"addNumber":0, "removeNumber":1, "sendSMS": 2, "sendVoiceCall":3, "addClient":4, "removeClient":5, "option1":6, "option2":7}

# this class handles the options field for each packet
class Options(object):

	# initializes the options
	def __init__(self):
		self._bits = 0

	@property
	def addNumber(self):
		return 1 & (self._bits >> _BITMAP["addNumber"])
	# keeps the numeric representation in sync with the current settings
	@addNumber.setter
	def addNumber(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["addNumber"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["addNumber"]))

	@property
	def removeNumber(self):
		return 1 & (self._bits >> _BITMAP["removeNumber"])
	@removeNumber.setter
	def removeNumber(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["removeNumber"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["removeNumber"]))

	@property
	def sendSMS(self):
		return 1 & (self._bits >> _BITMAP["sendSMS"])
	@sendSMS.setter
	def sendSMS(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["sendSMS"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["sendSMS"]))

	@property
	def sendVoiceCall(self):
		return 1 & (self._bits >> _BITMAP["sendVoiceCall"])
	@sendVoiceCall.setter
	def sendVoiceCall(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["sendVoiceCall"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["sendVoiceCall"]))

	@property
	def addClient(self):
		return 1 & (self._bits >> _BITMAP["addClient"])
	@addClient.setter
	def addClient(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["addClient"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["addClient"]))

	@property
	def removeClient(self):
		return 1 & (self._bits >> _BITMAP["removeClient"])
	@removeClient.setter
	def removeClient(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["removeClient"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["removeClient"]))

	@property
	def option1(self):
		return 1 & (self._bits >> _BITMAP["option1"])
	@option1.setter
	def option1(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["option1"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["option1"]))

	@property
	def option2(self):
		return 1 & (self._bits >> _BITMAP["option2"])
	@option2.setter
	def option2(self, val):
		if (val):
			self._bits = self._bits | (1 << _BITMAP["option2"])
		else:
			mask = 0b0
			numOpts = len(_BITMAP)
			for i in xrange(0, numOpts):
				mask = 1 | mask << 1
			self._bits = self._bits & (mask ^ (1 << _BITMAP["option2"]))

	@property
	def bits(self):
		return self._bits
	@bits.setter
	def bits(self, val):
		self._bits = val

# base class of the packets. This class handles the options and sequences
class Packet(object):
	# initializes the class
	def __init__(self):
		self.options = Options()
		self.payload = 0
		self.seqNum = 0
	
	# packs the packet into a representation of bytes using struct.pack()
	@property
	def toBytes(self):
	# ! says to use Network-byte order
	# H says to use unsigned short
	# B says use unsigned char
		return struct.pack("!HB", self.seqNum, self.options.bits)
	
	def fromBytes(self, bits):
	# unpacks a packet from the given bits
		pass

# builds the class to handle client add or remove
class ClientPacket(Packet):
	# initializes the class
	def __init__(self):
		self.clientID = 1
		self.serverSecret = 0

# builds the class to handle adding or removing phone numbers
class NumberPacket(Packet):
	# initializes the packet
	def __init__(self):
		self.number = 0

# builds the class to handle sending a notification to a customer
def NotifyPacket(Packet):
	# initializes the packet
	def __init__(self):
		self.number = 0
		self.greetNumber = 1
		self.greeting = "Hello."

if __name__ == "__main__":
	opt = Options()
	opt.addNumber = 0
	opt.removeNumber = 0
	opt.sendSMS = 0
	opt.sendVoiceCall = 0
	opt.addClient = 1
	opt.removeClient = 0
	opt.option1 = 1
	opt.option2 = 9
	packet = Packet()
	packet.options = opt
	print "%s" % packet.toBytes
