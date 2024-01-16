from scapy.all import *

# Build an IP datagram
d = IP(dst="8.8.8.8") / ICMP(type=8)

# Send the datagram and receive the reply
r = sr1(d, timeout=3)

# Show some fields
print(r)
