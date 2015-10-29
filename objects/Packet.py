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
	
	def __repr__(self):
	# returns the binary view of these options
		return "{:08b}".format(self._bits)

	@property
	def bits(self):
		return self._bits
	@bits.setter
	def bits(self, val):
		self._bits = val

# base class of the packets. This class handles the options and sequences
class Packet(object):
# handles packet operations
	# variable used to determine packing sequence
	# ! says to use Network-byte order
	# H says to use unsigned short
	# B says use unsigned char
	PACK_SEQUENCE = "!HB"

	# the length of the sequence number
	LEN_SEQ_NUM = 2
	#the length of the options field
	LEN_OPT_FIELD = 1

	# initializes the class
	def __init__(self):
		self.options = Options()
		self.seqNum = 0
	
	# packs the packet into a representation of bytes using struct.pack()
	@property
	def packedBytes(self):
	# packs the bytes using the sequence packing scheme
		return struct.pack(Packet.PACK_SEQUENCE, self.seqNum, self.options.bits)
	
	def unpackBytes(self, bits):
	# unpacks a packet from the given bits
		self.seqNum, self.options.bits = struct.unpack(Packet.PACK_SEQUENCE, bits)
	
	def __repr__(self):
	# returns a string representation of this object
		return "{:02x}:{:1x}".format(self.seqNum, self.options.bits)

	@staticmethod
	def parseBytes(bits):
	# parses the given bytes into a packet and returns the 
	# fully formed packet
	# returns: fully formed packet of the type determined by the options field
		options = int(struct.unpack("!B", bits[2:3])[0])
		if((options  & 0b01) == 1 or (options & 0b10 == 2)): # check if number packet
			packet = NumberPacket()
			packet.unpackBytes(bits)
			return packet
		elif((options >>2  & 0b01) == 1 or (options>>2 & 0b10 == 2)): # check if notify packet
			packet = NotifyPacket()
			packet.unpackBytes(bits)
			return packet
		elif((options >> 4) & 0b11 == 1 or ((options >> 4) & 0b11 == 2)): # check if client packet
			packet = ClientPacket()
			packet.unpackBytes(bits)
			return packet

	@staticmethod
	def decryptPacket(encrData):
	# decrypts a packet given the encrypted payload
	# return:	returns a defined packet (with the appropriate child class)
	#			with its values set to the decrypted results
		return Packet.parseBytes(encrData)

# builds the class to handle client add or remove
class ClientPacket(Packet):
# manages a packet for adding/removing clients
	# I says to use unsigned integer
	# 8Q says to use 8 unsigned long longs
	PACK_SEQUENCE = "".join([Packet.PACK_SEQUENCE, "I"])
	LEN_CLIENT_ID = 4
	#the offset of the secret from beginning of the byte sequence
	SECRET_OFFSET = Packet.LEN_SEQ_NUM + Packet.LEN_OPT_FIELD + LEN_CLIENT_ID

	# initializes the class
	def __init__(self):
		super(ClientPacket, self).__init__()
		self.clientID = 0
		self.serverSecret = "\x00"

	def __repr__(self):
	# returns a string representation of this object
		return "{:02x}:{:1x}:{:0>4x}:{:}".format(self.seqNum, self.options.bits, self.clientID, self.serverSecret)

	# packs the packet into a representation of bytes using struct.pack()
	@property
	def packedBytes(self):
	# returns the packed sequence of bytes according to the add/remove
	# client packet in the specification
		return struct.pack(ClientPacket.PACK_SEQUENCE, 
			self.seqNum, 
			self.options.bits, 
			self.clientID) + (bytes(self.serverSecret))
	
	def unpackBytes(self, bits):
	# unpacks a packet from the given bits
	# expects the bits to be packed in the same manner
		self.seqNum, self.options.bits, self.clientID = struct.unpack(ClientPacket.PACK_SEQUENCE, bits[:ClientPacket.SECRET_OFFSET])
		self.serverSecret = bits[ClientPacket.SECRET_OFFSET:]

# builds the class to handle adding or removing phone numbers
class NumberPacket(Packet):
# manages a number packet
	# the packing sequence
	# I says to use unsigned integer
	PACK_SEQUENCE = "".join([Packet.PACK_SEQUENCE, "I"])

	# initializes the packet
	def __init__(self):
		super(NumberPacket, self).__init__()
		self.number = 0
	
	def __repr__(self):
	# returns a string representation of this object
		return "{:02x}:{:01x}:{:0>4x}".format(self.seqNum, self.options.bits, self.number)

	@property
	def packedBytes(self):
	# returns the packed sequence of bytes according to the add/remove
	# number packet in the specification
		return struct.pack(NumberPacket.PACK_SEQUENCE, 
			self.seqNum, 
			self.options.bits, 
			self.number)
	
	def unpackBytes(self, bits):
	# unpacks the packet from the given bits
		self.seqNum, self.options.bits, self.number = struct.unpack(NumberPacket.PACK_SEQUENCE, bits)

# builds the class to handle sending a notification to a customer
class NotifyPacket(Packet):
# manages an SMS send packet
	# the packing sequence to use
	PACK_SEQUENCE = "".join([Packet.PACK_SEQUENCE, "IH"])

	# the length in bytes of the phone number
	LEN_PHONE_NUMBER = 4
	# length in bytes of the number in this greeting
	LEN_GREETING_NUMBER = 2
	# offset at which the greeting starts
	OFFSET_GREETING = Packet.LEN_SEQ_NUM + Packet.LEN_OPT_FIELD + LEN_PHONE_NUMBER + LEN_GREETING_NUMBER
	# initializes the packet
	def __init__(self):
		super(NotifyPacket, self).__init__()
		self.number = 0
		self.greetNumber = 1
		self.greeting = "Hello."

	def __repr__(self):
	# returns a string representation of this object
		return "{:02x}:{:1x}:{:0>4x}:{:0>2d}:{}".format(self.seqNum, self.options.bits, self.number, self.greetNumber, self.greeting)

	@property
	def packedBytes(self):
	# returns the packed sequence of bytes according to the add/remove
	# number packet in the specification
		return struct.pack(NotifyPacket.PACK_SEQUENCE, 
			self.seqNum, 
			self.options.bits, 
			self.number,
			self.greetNumber) + bytes(self.greeting)
	
	def unpackBytes(self, bits):
	# unpacks the packet from the given bits
		self.seqNum, self.options.bits, self.number, self.greetNumber = struct.unpack(NotifyPacket.PACK_SEQUENCE, bits[:NotifyPacket.OFFSET_GREETING])
		self.greeting = str(bits[NotifyPacket.OFFSET_GREETING:])

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
