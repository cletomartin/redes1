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


### Format

### Fragmentation

### Addressing

### Subnetting

## Configuration and management protocols

#### ICMP

#### DHCP

## IP routing


### Delivery

### Forwarding

### Routing tables

### Dynamic routing

## Exercises
> TBD
