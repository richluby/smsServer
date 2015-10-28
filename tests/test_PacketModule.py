#!/usr/bin/python

import unittest
from objects import *

class TestPacketModule(unittest.TestCase):
# tests the Packet module for correctness
	def setUp(self):
	# establishes a know options configuration
		self.options = Options()
		self.options.bits = 0b00001111

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
