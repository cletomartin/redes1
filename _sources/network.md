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

```{note}
The DIY examples:

- We use `ping` for sending 1 ICMP packet with 4000 bytes of data. Note that the MTU is 1500 bytes.
  `tshark` is used for capturing traffic. It shows that the datagram is split in 3 fragments.

  `ping` is actually sending 4028 bytes: 4000 bytes of data, 20 bytes for the IP header and 8 bytes corresponding to the ICMP header.

- In this case, the ICMP packet contains 3992 bytes of data, thus it is sent 4020 bytes (including the IP and ICMP headers).

- Here we use a Python library called scapy for generating an IP datagram. We add a payload of 7000 bytes and this generates 5 fragments.
  You can find the [code here](src/scapy/frag.py).
```

### Addressing

The IP protocol addresses are 32-bit integers.
Each node of an IP network will have, at least, one IP address that will identify it _uniquely_ within the network.
Note that a node can belong to multiple networks (like a router) so it could have multiple IP addresses associated to it.

The addresses are hierarchical, similar to a postal address (e.g. country/city/street).
The 32 bits that make the IP address are divided in 2 groups:

- _Prefix_: that identifies the _network_.
- _Suffix_: that identifies the _host_ within that network.

```{note}
For example, the address `192.168.1.128` with a prefix of n=24, the network is `192.168.1` and the host is `128` within that network.
However, if n=8 the network is `192` and the host would be `168.1.128`.
```

There are a few special addresses:

- `0.0.0.0`: indicates _this host_. Its meaning might vary depending the context it is used.
  For example, it might indicate that a service can listen on _any_ interface of the host.
  In DHCP, as we will see, refers to the host that is requesting an IP address.
- `255.255.255.255`: is the broadcast address. Any message send to this direction will be received by all hosts.
- `X.X...0000`: is the network address. It is the first address of the range defined by the prefix.
- `X.X...1111`: is the broadcast address within the network. It is the last address of the range defined by the prefix.
- `0.0...X`: identifies a host within the network.
- `127.0.0.0`: the loopback network used for testing network applications without the need of using real Internet connection.

Originally, the Internet was divided in classes:

- _Class A_: start with `0` and uses 8 bits for the prefix.
- _Class B_: start with `10` and uses 16 bits for the prefix.
- _Class C_: start with `110` and uses 24 bits for the prefix.
- _Class D_: start with `1110` and use for multicast addresses.
- _Class E_: start with `1111` and reserved for future use.

```{note}
Classful addressing is now _obsolete_ because it couldn't fit well to address demand.
The class A addresses provide a ver large range of hosts that can be in the network ($2^24$)
but only 128 networks can be defined.
The class C only provides 256 host addresses but the next step (the class B) provides $2^16$.
Organisations and companies that need to go from C to D might not make a good use of all that range.

In general terms, classful addressing makes the address ranges to be not well used and do not adapt to the real demand.
```

Currently, the Internet uses classless addressing, where we just need to fix the prefix lentgh _n_ to fully define a network address.
We can define this _n_ as we wish, based on our needs, so very little amount of addresses will be wasted.
The notation of an address will be: `XXX.XXX.XXX.XXX/n`.

```{note}
In the example of `167.199.170.82/27`:

- There allows a block of $2^5$ addresses.
- The first one is the network address: `167.199.170.64`
- The last one is the network broadcast address: `167.199.170.95`
- Note that `167.199.170.64` and `167.199.170.95` are _not_ used for hosts.
  So for addressing hosts in that range we would have $2^5 - 2$ addresses.
- `167.199.170.82` is the address of the host and, for example, `167.199.170.195` do not belong to this network.
```

Routers forward datagrams from one network to another, depending on the destination IP.
This is an operation that must be quick because they will be doing _a lot_.
In order to know what is the network address of a given IP can use the concept of _network mask_.
The mask is a 32-bit number where the first _n_ bits (the length of the prefix) are set to 1 and the rest to 0.
For example: `167.199.170.82/27` has a mask of `11111111.11111111.11111111.11100000`.
By using this mask, it is only required an `AND` operation to get the network address:

```
167.199.170.82   -  10100111.11000111.10101010.01010010
255.255.255.224  -  11111111.11111111.11111111.11100000
-------------------------------------------------------
                    10100111.11000111.10101010.01000000  - 167.199.170.64
```

In classless addressing, the IP must be provided along its mask. That way, the host is fully defined in the Internet.
`IP/mask` format is known as _CIDR notation_.
Classless Inter-Domain Routing (CIDR) is a method of allocating IP addresses which was created for replacing the classful approach of the Internet.
IANA delegates the assignation of the IP addresses world-wide by providing different ranges to local entities like ISPs or similar companies.
As we have seen, CIDR is based on _VLSM_ where the network mask can be of different length to provide accurate ranges for different needs without wasting too many IPs.

There has been defined a few IP addresses for private use.
These means that these IP ranges will not go through the public Internet and can be used within an organisation:

- `10/8`
- `172.16/12`
- `192.168/16`

There are also the _link-local addresses_ that are used for automatic configuration of the hosts in a network: hosts without an IP address select an IP address from the range `169.254/16`.
Although these addresses will never go to the Internet, they can be useful for contacting neighbours though.

### Subnetting

Subnetting is the process of subdividing a network into smaller networks so the IPs provided by the original range can be better used.
If you ever get assigned to a class A or B, it is clear that the amount of hosts available in that range could be excessive for your needs.
Using subnetting you can split the available space into sub-networks.
Each sub-network could also be split in other sub-sub-networks and so on.
This way, it is possible to organise a big range of IPs and make better use of the available addresses for hosts on each network.

```{note}
In the example:

- The orginal n is 16 (a class B network).
- We use 4 bits more for creating subnets.
  This means we can have up-to 16 subnets ($2^4$).
- Each sub-net will be able to address $2^{32 - 20} - 2$ hosts.
  Note we substract 2 because we need network and broadcast addresses.
```

Because we _extend_ the prefix length to create subnets, the number of possible subnets will be always power of 2.
I can be applied to any block as long as it is not used already.

```{note}
In the example we need to build 4 subnetworks for the network 141.14.0.0/24.
This means that we will need to use 2 bits more, so the resulting subnets will be `/26` but with different values of course.

- 141.14.0.`00 000000`/26
  - 141.14.0.`00 000000` -> 141.14.0.0/26 net
  - 141.14.0.`00 111111` -> 141.14.0.63/26 brd
- 141.14.0.`01 000000`/26
  - 141.14.0.`01 000000` -> 141.14.0.64/26 net
  - 141.14.0.`01 111111` -> 141.14.0.127/26 brd
- 141.14.0.`10 000000`/26
  - 141.14.0.`10 000000` -> 141.14.0.128/26 net
  - 141.14.0.`10 111111` -> 141.14.0.191/26 brd
- 141.14.0.`11 000000`/26
  - 141.14.0.`11 000000` -> 141.14.0.192/26 net
  - 141.14.0.`11 111111` -> 141.14.0.255/26 brd
```

## Configuration and management protocols

In this section we are going to explain two important protocols that help the network layer in some sense.

### ICMP

IP is a network protocol that delivers datagrams. This delivery, even it is not reliable, requires some basic mechanisms to detect errors, network congestions, etc.
The Internet Control Message Protocol (ICMP) works on top of IP to provide:

- _Error detection_ at multiple levels.
- _Information_ about the network status (hosts, routers, etc).

Each ICMP message is encapsulated in an IP datagram and the message format is as follows:

- _ICMP Header_: the header is 8-byte long.
  - _Type_: 1 byte for the type of the ICMP message.
    An ICMP message can contain different information based on the type, a _request_, an _error_, a _reply_, etc.
    Depending of the value of this field it would be one or the other.

    | Type | Description             |
    |------|-------------------------|
    | 0    | Echo Reply              |
    | 8    | Echo Request            |
    | 3    | Destination Unreachable |

  - _Code_: 1 byte for the subtype of the ICMP message.
    For example code `1` of type `3` means the destination _port_ was unreachable,
    whereas code `1` of the same type means destination _host_ was unreachable.
  - _Checksum_: 2 bytes for the checksum that is calculated like the IP's checksum field.
  - _Rest of header_: 4 bytes more whose value will depend on the specific ICMP message.
- _ICMP Data_: the content of the message.

#### Errors

The ICMP errors are used for signalling problems.
They are always reported from the place they are generated _back to the source host_.
There are some special cases in which errors are not reported:

- An error of an ICMP message.
- IP datagrams failures with special addresses like 127.0.0.1 or multicast.
- A failure of an IP fragment that is not the first one.

```{note}
In all these cases, it is possible to generate lots of error messages.
```

For reference, the ICMP error messages have the following values in the ICMP Data field:
1. The IP header of the affected datagram, and
1. the first 8 bytes of the affected datagram's payload.

```{note}
In the [RFC 792](https://www.rfc-editor.org/rfc/rfc792) we can read:

:::
Internet Header + 64 bits of Data Datagram

      The internet header plus the first 64 bits of the original
      datagram's data.  This data is used by the host to match the
      message to the appropriate process.  If a higher level protocol
      uses port numbers, they are assumed to be in the first 64 data
      bits of the original datagram's data.
:::
```

Some examples of ICMP errors:

- _Destination unreachable_: sent by the router or host that detects the datagram cannot be delivered to its destination.
  The code provides more specific reasons.
- _Source quench_: a very basic congestion/flow control mechanism. Requests to the source to reduce the data rate.
- _Time exceeded_: sent by the router to indicate that found a TTL set to 0 or by a destination host where a fragmentation timeout expired (e.g. some piece is missing).
- _Parameter problem_: sent by the router or host indicating that a datagram was malformed or has missing fields.
- _Redirect_: typically sent by routers to hosts to inform them that there are better routes for an IP datagram.
  The host could update its routing table after receiving that information.
  For example, for a specific datagram, there might be a better route than the one used by a host.

#### Requests

Some examples of ICMP requests and replies:

- _Echo_: used to verify connectivity between 2 nodes. An Echo Request is replied by an Echo Reply.
- _Timestamp_: used to measure latency between 2 nodes.
- _Address mask_: used by a host to query the network address mask to use to a router.
- _Router Solicitation_: used by a host to identify what local routers are available around it.

```{note}
The example of `ping google.com` shows how to measure the round trip time (RTT).
This is the time between the Echo Request is sent and the Echo Reply is received.
```

```{note}
See the code of ping in Scapy [here](src/scapy/ping.py).
```

### DHCP

Dynamic Host Configuration Protocol (DHCP) is an application-layer protocol for assigning IP addresses to hosts automatically.
It follows the _client-server_ paradigm where the hosts (clients) request to the DHCP servers to be assigned with a configuration.
This configuration usually includes:
- An IP address.
- A network mask.
- A default gateway.
- A set of DNS name servers.

Less fequently the configuration can also include:

- A hostname.
- Date and time.

The format of a DHCP message is based on BOOTP as it was already widely used at the time DHCP was desgined:

- _Operation code_: 1 byte for telling if the message is a request or a reply.
- _HW type_: 1 byte to specify the hardware transmission medium.
- _HW address length_: 1 byte to specify how many bytes the hardware address is long. For Ethernet, this values is 6.
- _Hop count_: 1 byte to control the number of forwardings done by DHCP relays. Very similat to IP's TTL.
- _Transaction ID_: 4 bytes for an ID of the transaction. Randomly initialised by the client and repeated by the server.
- _Time elapsed_: 2 bytes to inform the number seconds since the client started.
- _Flags_: 2 bytes for flags. The first bit indicates if the message is unicast or multicast.
- _Client IP address_: the client IP. If the client does not know it, then `0.0.0.0` is used.
- _Your IP address_: the assigned client IP. This is set by the server.
- _Server IP address_: the server IP. If the client does not know it, then `255.255.255.255` is used.
- _Gateway IP address_: the default gateway associated to the network the client should use.

```{note}
The example of the DHCP operations can be explained as follows:

1. The client creates a `DHCPDISCOVER`. It does not know what DHCP servers are around.
   The message is sent to the broadcast address. Note that the source port and the destination port are fixec (68 and 67).
   We will see later why.

1. Every server that receieved the `DHCPDISCOVER` might reply with a `DHCPOFFER`.
   This message gives the client a possible configuration to use.
   Since the client does not have an IP yet, this message is sent to the broadcast address too.

1. The client might receive many `DHCPOFFER`. After that, it would select one of them and create a `DHCPREQUEST`.
   This request goes straight to the server that gave the offer to make sure that the configuration provided can be used for up-to `3600` seconds.

1. The server replies with a `DHCPACK` meaning that agrees with client's configuration request.

1. When the `DHCPACK` is received by the client, it can assume that it will be _bound_ for that IP address for the leased time period.

DHCP uses the fixed source port 68 in order to prevent other UDP applications to receive DHCP messages from servers.
Suppose an ephemeral port 12345 is used instead of 68.
If there is an UDP application running somewhere in the network at the same port,
the `DHCPOFFER` messages will arrive to this application too because they are all sent to the broadcast address.
```

```{note}
The state diagram shows how DHCP works. It is worth noting that the IP addresses are leased for a certain period of time.
It's client's reponsibility to renew these leases on time.
```

```{note}
You can run `sudo dhclient -v` to see how the DHCP client starts the renewal of the configuration.
Note that it will go to all interfaces of the computer.
```

## IP routing

In this section we are going to focus on how the hosts and routers manage the IP datagrams so they can reach their destination.

### Delivery methods

Every host of an IP network keeps a _routing table_.
This table contains the required information for sending IP datagrams based on their destination address.
The format of this table is as follows:

| Net Address | Mask | Delivery Method |
|-------------|------|-----------------|
| 11.11.11.0  | 24   | 10.0.0.5        |
| 10.0.0.0    | 8    | direct          |

In this example, there are 2 entries that can be read like this:

1. Any datagram sent to the 11.11.11.0/24 network (for example, to 11.11.11.45) should be sent to 10.0.0.5.
   This is likely to be a router that knows how to reach the destination host.
1. Any datagram sent to the 10.0.0.0/8 network (for example, to 10.10.0.1), it should be delivered directly.
   This means that the destination host is in the same network, so no need to send it to a router.

More formally, there are 2 delivery methods:

- _Direct_: if a datagram's destination is in the same network of the processing node then it is direct delivery.
- _Indirect_: the rest. This uses a _next-hop_ address where datagrams will be sent.

### Forwarding

Forwarding is the mechanismin where an IP datagram _is moved from one path to another_ during a route from its source to destation.
This requires:

- A _router_: which will move the datagram from one network to another.
- A _routing table_: which contains the information about the possible routes.
  Routers will query the routing table to make a decision about a specific datagram based on its destination address.

#### Methods

There are multiple methods that can implement a forwarding mechanism.
In this section we are going to compare some of them, listing the its pros and cons.

- _Route method_ vs _Next-hop method_: for each destination we could store:
  - The entire route: meaning that `A` needs to know `R1`, `R2` and finally `B`.
  - Just the next hop: meaning that `A` only needs to know `R1`.
	Note that `R2`'s next hop for reaching `B` is null because it would be direct delivery.

  Obviously, the next-hop method simplifies the routing tables that routers need to keep, so it seems a much better option.
  However, there is something good of having the entire route in the routing table: the context that the router has is bigger and could make smarter decisions (like foreseeing problematic branches).
  In any case, route method requires so much space and complexity to keep the routes up-to-date that it is not worth to implement.

- _Host-specific_ vs _Network-specific_: the destinations can be:
  - All the possible hosts: this means that `S` will have to store one row for `A`, `B`, `C`, and `D`.
  - Just the destination network: meaning that `S` will only need to store the destination network address to know how to each _any_ node from that network.

  Network-specific approach is better because simplifies the routing table and the process of updating them.

- _Default route_: a node or a router can be connected to a network that provide access to multiple inter-networks (like the Internet).
  We cannot store all the possible destination networks in our table.
  For that reason, the _default_ route can be placed at the end of the forwarding table.
  If the route for a given destination address is not found then the datagram will be forwarded to the next hop that pointed by the default route.

```{note}
We can define a forwarding mechanism in pseudo-code:

1. Get the destination address of the datagram.
1. Loop through each row of the routing table.
1. Perform an `AND` operation between the destination address and the network mask specified in the row.
1. If the result is equals to destination value of the row, then forward the datagram to the next hop.
1. If no row matched and there is a default route, then follow the default route.
1. If there is no a default route, then return an ICMP error stating that there is not a route for the given datagram.
```

### Routing tables

Given the previous procedure, each row in the routing table should contain the following fields:

- _Destination network address_: required to know what network address the route goes to.
- _Destination network mask_: required so the `AND` operation can be performed.
- _Next-hop address_: required to know what node will handle a matched datagram for this specific route.
- _Interface_: required to know through what interface the forwarded datagram should be sent.

The next-hop address and the interface is used downstream by ARP,
a link-layer protocol that translates an IP address to a link-layer address.
The link-layer address can be used by the link-layer to send frames containing the IP datagram.
We will study ARP in more detail in the following chapter.

```{note}
The example shows the routing table of the second router that has 2 interfaces: `eth0` and `eth1`.
`eth0` is connected to 40.0.0.0/8 network and its assigned IP is 40.0.0.8.
`eth1` is connected to 128.1.0.0/16 network and its assigned IP is 128.1.0.8.

Any datagram to any of the these networks will be considered for _direct delibery_ because the router is connected to them.
However datagrams to 30.0.0.0/8 network will need to be sent to 40.0.0.7 which has access to that network.
Datagrams to 192.4.10.0/24  will need to be sent to 128.1.0.9 for the same reason.

It is important to note that any other destination address, like 8.8.8.8, will generate an ICMP error because there is no route for it.
```

```{note}
The next example shows the routing table of R1 which has 3 interfaces.
In this case, a default route is configured.
```

```{note}
Based on the previous example, let's explain what it would happen if a datagram arrives to R1 with destionation address 180.70.65.140:

1. The first row's mask would be applied to the destination address:

   180.70.65.140 & 255.255.255.192 = 180.70.65.128

   It does not match the first row's destination field.

1. The second row's mask would be applied to the destination address:

   180.70.65.140 & 255.255.255.128 = 180.70.65.128

   In this case, it matches so the next-hop address and the interface is passed to ARP.
```

```{note}
Based on the previous example, let's explain what it would happen if a datagram arrives to R1 with destionation address 201.4.22.35:

1. The first row's mask would be applied to the destination address:

   201.4.22.35 & 255.255.255.192 = 201.4.22.0

   It does not match the first row's destination field.

1. The second row's mask would be applied to the destination address:

   201.4.22.35 & 255.255.255.128 = 201.4.22.0

   It does not match the first row's destination field.

1. The third row's mask would be applied to the destination address:

   201.4.22.35 & 255.255.255.0 = 201.4.22.0

   In this case, the result matches so the next-hop address and the interface is passed to ARP.
```


```{note}
Based on the previous example, let's explain what it would happen if a datagram arrives to R1 with destionation address 18.24.32.78:

All rows in the table will be queried and no one will provide a match except the latest one: the default route.
```

Now that each destination network address and mask need to be kept on each row,
one can think that in a real environment with lots of networks,
routers might need to keep lot of destination networks if neighbours are connected to multiple networks.

However, routers can use _address aggregation_ to simplify their routing tables.
Many network addresses can be collapsed into just one that includes many of them.
That way, only one table row is required to reach multiple networks.

```{note}
In the example, R1 is connected to 4 networks, all of them /26.
R2 does not need to know all those networks, it only needs one row for 140.24.7.0/24.

And it is /24 because R1 uses 2 bits for subnetting (/24 + 2 = /26).
```

However, address aggregation introduces a new problem.
What if one of the 4 networks is removed from R1 (for example, 140.24.7.192/26)  and now it is placed in a separated router.
Now R2 seems like it will not be able to use 140.24.7.0/24 in just one row.
It will need 2 rows: one for 140.24.7.0/24 and one for 140.24.7.192/26 because each of them are connected to different interfaces.
But one includes the other so both will match.

In order to disambiguate what row to pick the _longest mask matching_ criteria will be followed.
This means that the row in the routing table whose mask is the longest will be selected in case there are others shorter.
In our case, `/26` is longer than `/24` so both rows can coexist without any problem in R2.

```{note}
To see how this address aggregation provides a hierarchical routing, let's consider the following example:

- A regional ISP is assigned with 120.14.64.0/18. This means that it has $2^{16}$ addresses.
- This ISP divides this block in 4 to give each block to local 3 ISPs
  It needs 2 bits for subnetting. One block will not be used but the other 3 will be assigned to the local ISPs:
  1. 120.14.64.0/20: this local ISP subdivide this block in 8 subnetworks that will be assigned to small providers.
	 That requires 3 bits so the result in /23 networks:
	 - 120.14.64.0/23, to
	 - 120.14.78.0/23

	 And each of these small ISPs divide them into 128 blocks that will be assigned to households.
	 That requires 7 bits, so the resulting networks will be /30:

	 - 120.14.64.0/30 - ..., to
	 - 120.14.78.0/30 - ...

  1. 120.14.80.0/20: not assigned and reserved for future use.
  1. 120.14.96.0/20: this local ISP breaks down the network in 4 subnetworks, resulting in /22.
  1. 120.14.112.0/20: this local ISP breaks down the network in 16 subnetworks, resulting in /24.
```


### Dynamic routing

## Exercises
> TBD
