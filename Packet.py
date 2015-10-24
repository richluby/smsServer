#!/usr/bin/python

# this class handles the options field for each packet
class Options(object):
	# initializes the options
	def __inti__(self):
		self._addNumber = False
		self._removeNumber = False
		self._sendSMS = False
		self._sendVoiceCall = False
		self._addClient = False
		self._removeClient = False

	
