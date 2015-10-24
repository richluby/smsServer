<link rel="stylesheet" type="text/css" href="MD_styling.css" />

# SMS Server

This program provides a server that implements a key functionality for restaurant management: it notifies customers when the table is ready. The server receives phone numbers. Upon receiving a send packet, the server sends an SMS to the phone number listed.

The data is encrypted over the network using a one-time password, and the numbers themselves are stored strictly in RAM to alleviate customer privacy concerns.

## Packets

### Options

+-----+-----+-----------------------------+-----+--------------------------------+
| Bit | Val | Description                 | Val | Description                    |
+=====+=====+=============================+=====+================================+
|  0  |  1  | Add a number to list        |  0  | Do not add a number to list    |
+-----+-----+-----------------------------+-----+--------------------------------+
|  1  |  1  | Remove a number from list   |  0  | Do not remove number from list |
+-----+-----+-----------------------------+-----+--------------------------------+
|  2  |  1  | Send an SMS to the number   |  0  | Do not send an SMS             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  3  |  1  | Place a phone call          |  0  | Do not place a phone call      |
+-----+-----+-----------------------------+-----+--------------------------------+
|  4  |  1  | Add a client                |  0  | Do not add a client            |
+-----+-----+-----------------------------+-----+--------------------------------+
|  5  |  1  | Remove a client             |  0  | Do not remove a client         |
+-----+-----+-----------------------------+-----+--------------------------------+
|  6  |  1  | Developer specific          |  0  | Developer Specific             |
+-----+-----+-----------------------------+-----+--------------------------------+
|  7  |  1  | Developer Specific          |  0  | Developer specific             |
+-----+-----+-----------------------------+-----+--------------------------------+

Numbers that already exist will not be added a second time. Numbers that do not exist that are asked to be removed will not generate an error. Both cases will still generate an acknowledgement packet.

Bits 6-7 are provided for the developer to use in an implementation-specific manner. Information for developer options may go after the last specified field in a packet.

#### Client Management

A client in this context is the interface to the restaurant employee. The client should implement the ability to add or remove phone numbers, and send SMS or voice command packets. It should also implement the ability to add or remove a server from its list. 

### Adding or Removing a Client

+---------+----------+------------------+---------------+
|   SEQ   | Options  | Client ID        | Server Secret |
+=========+==========+==================+===============+
| 2 bytes | 0000XX-- | 4 bytes          | 64 bytes      |
+---------+----------+------------------+---------------+

**XX** is the sequence to determine if this client is being added or removed. The ID will be interpreted as a whole number. The Secret will be a salted, one-time hash of a shared secret between the server and any authorized clients. Bits 0-3 must be 0 to signal that a client operation is occurring.

### Adding or Removing a Phone Number

+---------+---------+------------------+
|   SEQ   | Options | Phone Number     |
+=========+=========+==================+
| 2 bytes | 1 byte  | 4 bytes          |
+---------+---------+------------------+

Sequence numbers can be defined in an implementation specific manner. No requirement exists for them to be monotonic nor deterministic. However, if the same number is used in short succession, then a packet may not be confirmed. When the server receives this packet, it will update each client using the same packet, albeit with a different sequence number.

### Sending an SMS

+---------+---------+------------------+--------------------+----------+
|   SEQ   | Options | Phone Number     | Number in Greeting | Greeting |
+=========+=========+==================+====================+==========+
| 2 bytes | 1 byte  | 4 bytes          | 2 bytes            | 64 bytes |
+---------+---------+------------------+--------------------+----------+

## Encryption

The entire packet is to be encrypted using a one-time password scheme. 
