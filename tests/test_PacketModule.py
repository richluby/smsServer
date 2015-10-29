#!/usr/bin/python

import unittest
from objects import *

class TestPacketModule(unittest.TestCase):
# tests the Packet module for correctness
	def setUp(self):
	# establishes a know options configuration
		self.options = Options()
		self.options.bits = 0b00001111

class TestPacketClass(TestPacketModule):
# test the Packet class
	def setUp(self):
	# sets up a known configuration
		self.packet = Packet()
		self.packet.options = Options()
		self.packet.payload = 0
		self.packet.seqNum = 0
	
	def test_representation(self):
	# tests the string return of the packet
		string = str(self.packet)
		self.assertEqual(string, "00:0")

	def test_packingBytes(self):
	#tests to verify that the payload packing and unpacking methods operate correctly
		self.packet.seqNum = 1
		self.packet.options.bits = 0b00001111
		packed = self.packet.packedBytes
		self.assertEqual(packed, '\x00\x01\x0f')
	
	def test_unpackingBytes(self):
	#test verifies that bytes are correctly unpacked
		unpacked = '\x00\x01\x0f'
		self.packet.unpackBytes(unpacked)
		self.assertEqual(self.packet.options.bits, 0b00001111)
		self.assertEqual(self.packet.seqNum, 1)
	
	@unittest.expectedFailure
	def test_parseClientPacket(self):
	# tests the ability to decrypt a client packet
		packet = ClientPacket()
		packet.options.addClient = True
		#print "\n",packet, packet.options.bits, "\n"
		newPacket = Packet.parseBytes(packet.packedBytes)
		self.assertIsInstance(newPacket, ClientPacket)

class TestClientPacketClass(TestPacketModule):
# test the client packet class
	def setUp(self):
		self.packet = ClientPacket()

	def test_packingBytes(self):
	# test packing the bytes
		self.packet.seqNum = 1
		self.packet.options.bits = 0b00001111
		self.packet.clientID = 1
		self.packet.serverSecret = "\xff"
		packed = self.packet.packedBytes
		self.assertEqual(packed, '\x00\x01\x0f\x00\x00\x00\x01\xff')

	def test_representation(self):
	# tests the string return of the packet
		string = str(self.packet)
		self.assertEqual(string, "00:0:0000:\xff")

	def testUnpackingBytes(self):
	#tests unpacking the bytes
		packed = '\x00\x01\x0f\x00\x00\x00\x01\xfd\xfa'
		self.packet.unpackBytes(packed)
		self.assertEqual(self.packet.seqNum, 1)
		self.assertEqual(self.packet.options.bits, 0b00001111)
		self.assertEqual(self.packet.clientID, 1)
		self.assertEqual(self.packet.serverSecret, "\xfd\xfa")

class TestNumberPacketClass(TestPacketModule):
# test the Packet class
	def setUp(self):
	# sets up a known configuration
		self.packet = NumberPacket()
		self.packet.seqNum = 0

	def test_representation(self):
	# tests the string return of the packet
		string = str(self.packet)
		self.assertEqual(string, "00:0:0000")

	def test_packingBytes(self):
	#tests to verify that the payload packing and unpacking methods operate correctly
		self.packet.seqNum = 1
		self.packet.options.bits = 0b00001111
		self.packet.number = 16
		packed = self.packet.packedBytes
		self.assertEqual(packed, '\x00\x01\x0f\x00\x00\x00\x10')
	
	def test_unpackingBytes(self):
	#test verifies that bytes are correctly unpacked
		unpacked = '\x00\x01\x0f\x00\x00\x00\x10'
		self.packet.unpackBytes(unpacked)
		self.assertEqual(self.packet.options.bits, 0b00001111)
		self.assertEqual(self.packet.seqNum, 1)
		self.assertEqual(self.packet.number, 16)

class TestNotifyPacketClass(TestPacketModule):
# test the Packet class
	def setUp(self):
	# sets up a known configuration
		self.packet = NotifyPacket()
		self.packet.seqNum = 0

	def test_representation(self):
	# tests the string return of the packet
		string = str(self.packet)
		self.assertEqual(string, "00:0:0000:01:Hello.")

	def test_packingBytes(self):
	#tests to verify that the payload packing and unpacking methods operate correctly
		self.packet.seqNum = 1
		self.packet.options.bits = 0b00001111
		self.packet.number = 16
		self.packet.greetNumber = 2
		self.packet.greeting = "Hello World"
		packed = self.packet.packedBytes
		self.assertEqual(packed, '\x00\x01'+ '\x0f'+'\x00\x00\x00\x10'+'\x00\x02'+'Hello World')
	
	def test_unpackingBytes(self):
	#test verifies that bytes are correctly unpacked
		unpacked = '\x00\x01'+ '\x0f'+'\x00\x00\x00\x10'+'\x00\x02'+'Hello World'
		self.packet.unpackBytes(unpacked)
		self.assertEqual(self.packet.options.bits, 0b00001111)
		self.assertEqual(self.packet.seqNum, 1)
		self.assertEqual(self.packet.number, 16)
		self.assertEqual(self.packet.greetNumber, 2)
		self.assertEqual(self.packet.greeting, "Hello World")

class TestOptionsClass(TestPacketModule):
# tests the Options class for correctness
	def setUp(self):
		self.options = Options()
		self.options.bits = 0b00000000

	def test_addNumber(self):
	# tests the return value
		self.options.addNumber = 1
		self.assertEqual(self.options.addNumber, 1, "addNumber not equal to 1")
		self.assertEqual(self.options.bits, 0b00000001)
		self.options.addNumber = 0
		self.assertEqual(self.options.addNumber, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_removeNumber(self):
	# tests the return value
		self.options.removeNumber = 1
		self.assertEqual(self.options.removeNumber, 1, "removeNumber not equal to 1")
		self.assertEqual(self.options.bits, 0b00000010)
		self.options.removeNumber = 0
		self.assertEqual(self.options.removeNumber, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_sendSMS(self):
	# tests the return value
		self.options.sendSMS = 1
		self.assertEqual(self.options.sendSMS, 1, "sendSMS not equal to 1")
		self.assertEqual(self.options.bits, 0b00000100)
		self.options.sendSMS = 0
		self.assertEqual(self.options.sendSMS, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_sendVoiceCall(self):
	# tests the return value
		self.options.sendVoiceCall = 1
		self.assertEqual(self.options.sendVoiceCall, 1, "sendVoiceCall not equal to 1")
		self.assertEqual(self.options.bits, 0b00001000)
		self.options.sendVoiceCall = 0
		self.assertEqual(self.options.sendVoiceCall, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_addClient(self):
	# tests the return value
		self.options.addClient = 1
		self.assertEqual(self.options.addClient, 1, "addClient not equal to 1")
		self.assertEqual(self.options.bits, 0b00010000)
		self.options.addClient = 0
		self.assertEqual(self.options.addClient, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_removeClient(self):
	# tests the return value
		self.options.removeClient = 1
		self.assertEqual(self.options.removeClient, 1, "removeClient not equal to 1")
		self.assertEqual(self.options.bits, 0b00100000)
		self.options.removeClient = 0
		self.assertEqual(self.options.removeClient, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_option1(self):
	# tests the return value
		self.options.option1 = 1
		self.assertEqual(self.options.option1, 1, "option1 not equal to 1")
		self.assertEqual(self.options.bits, 0b01000000)
		self.options.option1 = 0
		self.assertEqual(self.options.option1, 0)
		self.assertEqual(self.options.bits, 0b00000000)

	def test_option2(self):
	# tests the return value
		self.options.option2 = 1
		self.assertEqual(self.options.option2, 1, "option2 not equal to 1")
		self.assertEqual(self.options.bits, 0b10000000)
		self.options.option2 = 0
		self.assertEqual(self.options.option2, 0)
		self.assertEqual(self.options.bits, 0b00000000)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestPacketModule)

if __name__ == "__main__":
	unittest.verbosity = 2
	unittest.main()
