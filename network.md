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
  | 4     | IPv4     |
  | 6     | TCP      |
  | 17    | UDP      |
  | 89    | OSPF     |

- _Checksum_: 16 bits for detecting errors of the header.
  It needs to be checked on every hop of the route.
  The payload is not included and it is left to the upper layers to perform their own check.

  The field is computed by dividing the hearder in 2-byte fields, sum them all and complement the sum.
  If the final sum overflows, it is wrapped.

- _Source IP_: 32 bits for the source IP address.
- _Destination IP_: 32 bits for the destination IP address.
- _Options_: up-to 40 bytes is reserved for options that are used in specific scenarios and debugging.
  Although it is not mandatory to use options in the IP protocol, all IP devices should handle them if they are present.
  An option has the following structure:
  - _Code_: 8 bits for indicating the option
    - _Copy_: 1 bit for indicating whether the option needs to be copy or not to all the fragments.
    - _Class_: 2 bits for indicating the general category of the option.
    - _Number_: 5 bits for identifying the option. There are $2^5$ options avaiable but only a few of them are frequently used.
  - _Length_: 8 bits for specifiying the length of the data of this option.
  - _Data_: variable-length field containing the data of the option.

### Fragmentation

All networks are not the same.
Each network may have its own features and capabilities and an important one is the _Maximum Transfer Unit_ (MTU).
This is the maximum size of a frame that can be transmitted through a link. This value might be different from one network to another,
so routers will need to adapt the IP datagram size to it.

This process of routers slicing IP datagrams is known as _fragmentation_ and the IP protocol provides support to handle the problems associated with it.
At destination, the fragments are reassembled so the original IP datagram is built.

```{note}
The fragmentation can only happen at destination because intermediate routers might not see all the fragments passing through them.
Since IP datagrams might take different routes, because they are independent datagrams, only the destination is capable of reassembling them.
```

```{note}
The fragmentation example should be explained as follows:
- A datagram is going to be sent from `source` to `destination`.
- The router `R1` will have to fragment it in 3 fragments ($4020 / 1420 = 2.5$ so we need 3 fragments).
- `f1` and `f3`  will no need more fragmentation because the MTU will be enough for the rest of the hops.
- `f2` requires one more fragmentation step in `R4` as it goes to a smaller MTU.
- In total, 5 fragments will arrive.

In the following slide, you should explain how the data is distributed across the different fragments:

- An important aspect to take into account is that if the IP header is 20 bytes, these 20 bytes must be _always_ included.
  So `R1` will only be able to send 1400 bytes (plus 20 bytes of the IP header) through the bottom network.
  This is why the `f1` contains 1400 bytes (from 0 to 1399), `f2` contains 1400 bytes (from 1400 to 2799) and `f3` contains 1200 bytes (from 2800 to 3999).

  The identification field for all these fragments are the same as the original datagram (14567).

  The total length of each fragment changes to reflect the new size of the datagrams: 1420 (1400 + 20 for the header) for `f1` and `f2`, and 1220 for `f3`.

  The `M` bit is set to 1 for `f1` and `f2` but is set to 0 for `f3`. This bit indicates if there is more fragments to come. `f1` and `f2` has more fragments to come but `f3` is the last one.

  The last field that needs to be kept into account is the _fragmentation offset_.
  This field is calculated based on the first byte number of data of each fragment divided by 8:
  - `f1`: $0 / 8 = 0$
  - `f2`: $1400 / 8 = 175$
  - `f3`: $2800 / 8 = 350$

- `f2` is split in 2 more fragments: `f2.1` and `f2.2`. This would be a good exercise to calculate the different fields with the students.

   The original size of the datagram is 1400 bytes (plus 20 bytes for the header).
   The MTU is 820, so we can split this datagram is 2: `f2.1` of size 800 bytes (from 1400 to 2199) and `f2.2` of 600 bytes (from 2200 to 2799).

   The idenfication field remains the same.

   The total length now is set to 820 and 620 respectively.

   The fragment offset remains the same for `f2.1` ($1400 / 8$ was already calculated) but it is different for `f2.2` ($2200 / 8 = 275$).

   An important detail is that the `M` bit is 1 too all of them. `f2.2` is _not_ the last fragment of the original IP datagram,
   it is just another fragment within
```


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
