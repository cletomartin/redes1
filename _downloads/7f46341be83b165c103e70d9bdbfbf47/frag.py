from scapy.all import *

# Build an IP datagram
d = IP(dst="120.1.1.1")

# Set the payload: 7000 bytes
d.add_payload("Redes~1" * 1000)

# Send the datagram
send(d)
