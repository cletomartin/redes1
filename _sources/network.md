# Network layer

This lesson describes in depth the network layer. It descripts the IP addressing and routing mechanisms too.
You can find the slides [here](slides/network.odp).

Under the transport layer, the network layer is used mainly for delivering data between hosts
as long as the hosts are connected through a set of inter-networks.
The following are the main features of the network layer:

- _Payload encapsulation_: data from the transport layer is encapsulated and delivered to any point of the internet.
- _Routing_: the data packets are sent _host-to-host_ although they can travel through other hosts or networks.
  What route a packet takes is a decision made with the help of _routing protocols_ and it might the case that packets of the same transport flow go through different routes (_connectionless_).
- _Forwarding_: the _routing nodes_ of the network layer are known _routers_.
  They perform packet forwarding: decide what is the next hop based on the _routing table_.
- _Best-effort delivery_: the network layer is _unreliable_.
  There is no guarantee that a packet has arrived to destination nor it arrived in the right order.

```{note}
In the network example:

- The `Link` nodes are devices that only operates at data-link layer. They just connect nodes directly.
- The `Intermediate system` are nodes that can connect networks.
- A datagram going from the node `A` to any of the `End system` follows the encapsulation/decapsulation trace at the bottom of the image.
  Each node of the network uses up-to network layer.
```

```{note}
In this example, the _connectionless_ concepto is shown clearly.
Packets 1, 2, 3 and 4 take different routes and arrive out of order.
Note that this is a packet-switched network where information is transmitted as individual datagrams.
```

## IP protocol

The Inter-network Protocol (IP) is the standard network protocol of the Internet.
It can be used to interconnect different types of networks (made out of different technologies) as long as the nodes understand IP messages.

In this section we are going the dive into the format of the IP datagrams, the fragmentation mechinism, how IP addresses work and how they can be strucuture using subnetting.

### Format

The IP datagram has a maximum length of $2^16$ bytes:

- The minimum header length is 20 bytes. The header can be extended 40 bytes more with options.
- The rest is reserved to the payload.

These are the fields of the IP header:

- _Version_: 4 bits for specifying the IP version. `4` for IPv4 and `6` for IPv6.
- _Internet Header Length (IHL)_: 4 bits for specifying the length of the IP header in 4-byte words.
- _Type of Service_: 8 bits for helping to service differentiation (also known as _quality of service_)
- _Total Length_: 16 bits for specifying the total length of the IP datagram, including the header.
- _Identification_: 16 bits for identifying the datagram if it belongs to a fragmented one.
  If a datagram is fragmented, this field is the same for all the fragments.
- _Don't Fragment (DF)_: 1 bit to tell routers the datagram should not be fragmented.
- _More Fragments (MF)_: 1 bit to tell routers this datagram is not the last one of a serie of fragmented datagrams.
- _Offset_: 13 bits to tell the position of this datagram in the series of fragmented datagrams.
  It is expressed as a value of 8-byte words, so:
  - There can only be $2^8$ fragments.
  - The size of a fragment must be mutiple of 8, except for the last one.
  The first fragment has this value always set to 0.
- _Time-to-live (TTL)_: 8 bits to tell the router if a datagram needs to be discarded.
  Everytime a router forwards a datagram, it decreases the TTL value.
  If the value is set to 0, the packet is discarded by the router.

- _Protocol_: 8 bits to tell what protocol is encapsulated:

  | Value | Procotol |
  |-------|----------|
  | 1     | ICMP     |
  | 2     | IGMP     |
  | 4     | IP       |
  | 6     | TCP      |
  | 17    | UDP      |
  | 89    | OSPF     |


### Fragmentation

### Addressing

### Subnetting

## Configuration and management protocols

### ICMP

### DHCP

## IP routing


### Delivery

### Forwarding

### Routing tables

### Dynamic routing

## Exercises
> TBD
