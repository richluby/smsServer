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
	
	def testDecryptPacket(self):
	# tests decrypting a packet with zeroed options
		pass

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
	def test_returnValueAddNumber(self):
	# tests the return value of adding a number
		self.assertEqual(self.options.addNumber, 1, "addNumber not equal to 1")
	
	def test_returnValueRemoveNumber(self):
	# tests the return value of removing a number
		self.assertEqual(self.options.removeNumber, 1, "removeNumber not equal to 1")

	def test_returnValueSendSMS(self):
	# tests the return value of sending an SMS 
		self.assertEqual(self.options.sendSMS, 1, "sendSMS not equal to 1")

	def test_returnValueSendVoiceCall(self):
	# tests the return value of sending a voice call
		self.assertEqual(self.options.sendVoiceCall, 1, "sendVoiceCall not equal to 1")

	def test_returnValueAddClient(self):
	# tests the return value of adding a client
		self.assertEqual(self.options.addClient, 0, "addClient not equal to 0")
		
	def test_returnValueRemoveClient(self):
	# tests the return value of removing a client
		self.assertEqual(self.options.removeClient, 0, "sendVoiceCall not equal to 0")

	def test_returnValueOption1(self):
	# tests the return value of a developer option
		self.assertEqual(self.options.option1, 0, "option1 not equal to 0")

	def test_returnValueOption2(self):
	# tests the return value of a developer option
		self.assertEqual(self.options.option2, 0, "option2 not equal to 0")

	def test_returnValueBits(self):
	# tests the return value of a developer option
		self.assertEqual(self.options.bits, 0b00001111, "bits not equal to 0b00001111")
	
	def test_changeOptions(self):
	# test to ensure that the bit pattern is updated properly when the options change
		self.options.removeClient = True
		self.assertEqual(self.options.removeClient, 1, "removeClient not updated properly")
		self.assertEqual(self.options.bits, 0b00101111, "bit pattern not updated properly")

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(TestPacketModule)

if __name__ == "__main__":
	unittest.verbosity = 2
	unittest.main()
