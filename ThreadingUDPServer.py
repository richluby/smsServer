#!/usr/bin/python

import SocketServer

class ThreadingUDPHandler(SocketServer.BaseRequestHandler):
	# handles incoming items
	def handle(self):
		data = self.request[0].strip()
		print "I saw ", data, "from", self.client_address[0]

class ThreadingUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): pass
