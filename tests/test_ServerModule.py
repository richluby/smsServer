#!/usr/bin/python

import unittest, socket
import threading
from objects import *

class ServerBaseClass(unittest.TestCase):
# creates a server instance against which to check
	@classmethod
	def setUpClass(self):
	# creates a socket through which to send information
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serverAddress = ("localhost", 8657)
		self.clientID = 5643
		self.address = ("127.0.0.1", 6785)
		self.server = ThreadingUDPServer(self.serverAddress, ThreadingUDPHandler)
		serverThread = threading.Thread(target=self.server.serve_forever)
		serverThread.setDaemon(True)
		serverThread.start()
	
	@classmethod
	def tearDownClass(self):
	# closes the socket
		self.sock.close()
		self.server.close()
		
class TestServerModule(ServerBaseClass):
# tests the server Module
	def test_clientPacketHandler(self):
		packet = ClientPacket()
		packet.options.addClient = True
		packet.clientID = self.clientID
		self.server.handleClientPacket(packet, self.address[0])
		self.assertIn((packet.clientID, self.address[0]), self.server.connectedClients)
		packet.options.addClient = False
		packet.options.removeClient = True
		self.server.handleClientPacket(packet, self.address[0])
		self.assertNotIn((packet.clientID, self.address[0]), self.server.connectedClients)

	def test_numberPacketReceiver(self):
	# tests buidling the number packet
		packet = NumberPacket()
		packet.options.addNumber = True
		self.sock.sendto(packet.packedBytes, self.serverAddress)
		received = self.sock.recv(1024)
		packet = Packet.parseBytes(received)
		self.assertIsInstance(packet, NumberPacket)

	def test_clientPacketReceiver(self):
	# tests buidling the client packet
		packet = ClientPacket()
		packet.clientID = self.clientID
		packet.options.addClient = True
		self.sock.sendto(packet.packedBytes, self.serverAddress)
		received = self.sock.recv(1024)
		packet = Packet.parseBytes(received)
		self.assertIsInstance(packet, ClientPacket)

	def test_notifyPacketReceiver(self):
	# tests buidling the notify packet
		packet = NotifyPacket()
		packet.options.sendSMS = True
		self.sock.sendto(packet.packedBytes, self.serverAddress)
		received = self.sock.recv(1024)
		packet = Packet.parseBytes(received)
		self.assertIsInstance(packet, NotifyPacket)
