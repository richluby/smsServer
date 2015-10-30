#!/usr/bin/python

import SocketServer, logging, socket
from objects import *
from Packet import *
from collections import OrderedDict

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

class ThreadingUDPHandler(SocketServer.BaseRequestHandler):
# handles receiving data
	def __init__(self, request, client_address, server):
	# initializes the logger
		self.logger = logging.getLogger("UDPHandler")
		SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
		return

	# handles incoming items
	def handle(self):
		data = self.request[0].strip()
		try:
			packet = Packet.decryptPacket(data)
			self.server.handlePacket(packet, self.client_address)
			self.logger.debug("I saw %s from %s", packet, self.client_address[0])
		except ValueError:
			self.logger.info("Invalid checksum from %s.", self.client_address[0])

class ThreadingUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): 
# serves the sms server
	# defines the maximum number of ACK packets to check in memory
	MAX_ACKS = 50

	def __init__(self, serverAddress, handler):
	# initializes the logging interface
		self.logger = logging.getLogger("Server")
		self.logger.info("Initializing server for %s.", serverAddress)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.packetDict = OrderedDict()
		self.connectedClients = set()
		SocketServer.UDPServer.__init__(self, serverAddress, handler)
	
	def secretIsValid(self, secret):
	# checks if the provided secret is valid
	#TODO
		return True

	def handleNumberPacket(self, packet):
		self.logger.info("NumberPacket: %s", packet)
	
	def handleNotifyPacket(self, packet):
	# sends a notification to the given number
	# this method will change depending on the vendor chosen
	# for the SMS/Phone service
		self.logger.info("NotifyPacket: %s", packet)
	
	def handleClientPacket(self, packet, ipAddress):
	# handles a client packet
	# packet:		the packet that provides the client information
	# ipAddress:	the (ip, port) of the client
		self.logger.info("ClientPacket: %s", packet)
		if (packet.options.addClient and self.secretIsValid(packet.serverSecret)):
			self.connectedClients.add((packet.clientID, ipAddress))
			self.logger.info("%d at %s connected.", packet.clientID, ipAddress[0])
		elif (packet.options.removeClient and self.secretIsValid(packet.serverSecret)):
			self.connectedClients.discard((packet.clientID, ipAddress))
			self.logger.info("%d at %s disconnected.", packet.clientID, ipAddress[0])

	def handlePacket(self, packet, clientAddress):
	# handles parsing an individual packet
		if isinstance(packet, NumberPacket):
			self.handleNumberPacket(packet)
		elif isinstance(packet, NotifyPacket):
			self.handleNotifyPacket(packet)
		elif isinstance(packet, ClientPacket):
			self.handleClientPacket(packet, clientAddress[0])
		if (packet.seqNum not in self.packetDict):
			self.sock.sendto(packet.packedBytes, clientAddress) 
	
	def close(self):
	# closes the socket associated with the server
		self.socket.close()
		self.sock.close()
		self.logger.info("Server closed.")
