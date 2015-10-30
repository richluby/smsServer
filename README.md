SMS Server
=============

This poject aims to provide an SMS server to a system. The server receives phone numbers and customization options, places those customizations into a generic message, and then sends an SMS or voice call to the phone number.

Use cases include notification systems such as emergency situations or a restaurant informing its customers that the table is ready.

# Navigating the Project

The specification for the communication protocol is in the [specification.md](#docs/specification.md) document. The docuement describes the means by which to communicate with the server, and is intended to allow creating a client that interfaces with the server.

The server can be started with [sendSMSServer.py](#sendSMSServer.py). The file supports a "-h" option. Configurations can be placed in the (smsServer.conf)[#smsServer.conf] file, and will override command-line arguments. 

The (tests)[#tests] directory contains functional tests for each function in the system. Many of of the tests will also have minimal working examples of different aspects of the program; these can provide aid when designing something related to the project.

All object files are contained in the (objects)[#objects] directory. (Packet.py)[#Packet.py] contains the classes for handling the packets as defined in the specification. It also contains the Options class to simplify handling options for a particular class. (ThreadingUDPServer.py)[#ThreadingUDPServer.py] holds the server instance. This module provides the necessary functionality to run the program.
