# SMS Server

This program provides a server that implements a key functionality for restaurant management: it notifies customers when the table is ready. The server receives phone numbers. Upon receiving a send packet, the server sends an SMS to the phone number listed.

The data is encrypted using a one-time password, and the numbers themselves are stored strictly in RAM to alleviate customer privacy concerns.

## Packets

### Options

| Bit | Val | Description                 | Val | Description 
+-----+-----+-----------------------------+-----+--------------------------------+
|  0  |  1  | Add a number to the list    |  0  | Remove a number from the list  |
+-----+-----+-----------------------------+-----+--------------------------------+
|  1  |  1  | Send an SMS to the number   |  0  | Place a phone call             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  2  |  1  | Reserved for future use     |  0  | Reserved for future use        |
+-----+-----+-----------------------------+-----+--------------------------------+
|  3  |  1  | Reserved for future use     |  0  | Reserved for future use        |
+-----+-----+-----------------------------+-----+--------------------------------+
|  4  |  1  | Developer specific          |  0  | Developer Specific             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  5  |  1  | Developer Specific          |  0  | Developer specific             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  6  |  1  | Developer Specific          |  0  | Developer specific             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  7  |  1  | Developer Specific          |  0  | Developer specific             |
+-----+-----+-----------------------------+-----+--------------------------------+

Numbers that already exist will not be added a second time. Numbers that do not exist that are asked to be removed will not generate an error.

Bits 2-3 are reserved for future specification expansion. Bits 4-7 are provided for the developer to use in an implementation-specific manner. 

### Adding or Removing a Phone Number

+---------+------------------+
| Options | Phone Number     |
+=========+==================+
| 1 byte  | 4 bytes          |
+---------+------------------+

### Sending an SMS

+---------+------------------+--------------------+---------
| Options | Phone Number     | Number in Greeting | Greeting
+=========+==================+====================+=========
| 1 byte  | 4 bytes          | 2 bytes            | 64 bytes
+---------+------------------+--------------------+---------

### Updating the Clients

The server updates the clients (maitre d') after each number is received. While this is fine for a few numbers, it will start to overload a network given many (>100) numbers that are constantly being updated. 

## Encryption

The entire packet is to be encrypted using a one-time password scheme. 
