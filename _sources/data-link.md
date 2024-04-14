# Data-link layer

This lesson describes in depth the data-link layer. It descripts its functionality, the link-layer addressing and ARP.
You can find the slides [here](slides/data-link.pdf).

The data-link layer (or just link layer) is in charge of the _node-to-node_ communication.
It is important to note that the _domain_ of the link layer is limited to the nodes that are _directly_ connected.
This means there is _no mediators_ in the communication provided by this layer.

It is located under the network layer, so it receives/sends _frames_ of data that are going to be used by the network layer.
It is also located on top of the physical layer so it does not deal with the transformation of the data into the physical signals that will be sent through the communication medium.
However, it will have to deal with some problems that the physical medium generates like transmission errors, propagation delays, etc.

## Functionality

The data-link layer is usually divided in 2 sublayers that perform operations at different abstraction layer:

1. The _data link control_ layer (DLC): focused on error and flow control on both point-to-point and broadcast links.
1. The _media access control_ layer (MAC): focused on the problems associated with sharing a medium like a broadcast links.
   This sublayer is not required in those situations where only point-to-point links are used.

### Framing

The first fundamental service that provided is _framing_.
The PDU is called _frame_. The network datagrams are encapsulated in frames that are going to be sent to the destination.
In the destination, those frames are going to be decapsulated and passed the transported datagram to the network layer.
The _intermediate nodes_ perform these 2 operations all the time.
This is required because:

- They connect two different physical technologies
- The addresses between link domains are different, so the frames need to be updated.

Each frame has the following parts (shown in the slide):

- _Flag_: used at the beginning and at the end of the frame to mark when it starts and when it ends.
  The byte `01111110` is used for this.
- _Header_: with the source and destination addresses, sizes, etc.
- _Payload_: the data coming from the network layer.
- _Trailer_: typically used for error checking.

```{note}
This framing process can be seen as our _postal_ code.
When we put a message in an envelope, we are delimiting the information to be transported in a _frame_ (the envelope).
```

The frame size can be:
- _Fixed_: in which case there is no need of using any kind of delimiters as the fixed size itself can be used to distinguish different frames.
  ATM (mostly used for WAN connections) uses this type of fixed frames called _cells_.
- _Variable_: prevalent in LAN environments and need the use of delimiters.
  We have seen that we are going to use a known flag as a delimiter but: what would it happen if the flag is part of the network data?
  In order to solve this problem, an _escape_ value is used:
  1. If FLAG is in the data, then add a special value ESC in front of it.
  1. If ESC is also in data, then add ESC again as a prefix to avoid it.

  Since this is done at byte level, this technique is known as _byte stuffing_.
  This process is performed for every single FLAG or ESC by found in the data.

  ```{note}
  In the figure, the data contains FLAG and ESC.
  The generated frame will have `ESC FLAG` and `ESC ESC`.
  When this frame is received, the receiver will just to remove the escaping characters to get the original data.
  ```
  Since process is done at byte level, it does not work well with today's data encoding like Unicode that uses 16 or 32 bits.
  For this reason, most of the protocols perform the this escaping technique at bit level. This is known as _bit stuffing_:
  ```{note}
  Since de flag is `01111110`, the algorithm for escaping a problematic sequence goes as this:

  - If `0 11111` is found in the data then a `0` is appended to avoid matching the FLAG.
    Then the next bit is added normally.
  - If the receiver detects `0 11111 0`, then it transforms it to `0 11111`.
  - The real flag is never stuffed so there is no possible conflict.
  ```

### Flow control and congestion control

As we have seen in other layers, a frame producer can overwhelm a receiver if the number of frames pushed from the first one to the second one is too fast.
The link layer provides flow control by:

- Using buffers on both sides so those frames that cannot be processed at a certain time can be done later.
- Use control frames for signalling the producer to reduce the transmission rate.

### Error control

The physical layer is not reliable.
Even technologies like fibre optic can produce transmission errors and corrupt data while sending bits through the transmission medium.
In order to detect this kind of problems, a _Cyclic Redundancy Check_ (CRC) is added to the frames by the sender and tested by the receiver.
This is very similar to the checksum fields we have seen so far.
If a corrupted frame is silently discarded, meaning that the network layer will not receive any of those.
For those that are _not_ corrupted it needs to:
1. Pass it to the network layer,
1. Optionally, signal the sender with an ACK frame that the sent frame was received correctly.
   This approach is also related with the flow control.

### Connectionless and connection-oriented

Depending on the protocol used, the data transmission can happen:

- _Connectionless_: where each frame is independent from each other and it is independent from the others.
  Most wired LAN protocols use this.

- _Connection-oriented_: where the establishment of a connection is required prior the data transmission.
  Some WLAN protocols and point-to-point WAN protocols use this approach.

## Ethernet

This was the first LAN protocol in history designed by Xerox in 1976 and made it available in 1980.
The IEEE organisation started a project in 1985 called "Project 802" to define the link layer of the Internet stacks (OSI and TCP/IP).
They subdivided the data-link in 2 sublayers:

- The _logical link control_ (LLC): similar to our already known DLC.
  LLC is optional if the upper-layer protocols do not need them.
  For TCP/IP traffic, they are not usually required.
- The _media access control_ (MAC): similar to our already known MAC.
  In Ethernet, this layer is always present.

Ethernet is one of the few protocols that have survived since the very beginning and today is common to find LANs at 10Gbps which is the forth generation.
Ethernet is connectionless and unreliable:
- It does not require the creation of a connection.
- Frames can overwhelm the receiver and being discarded silently.
  Frames can also be corrupted and the will be discarded silently.
  If frames are discarded the sender will never know.
  ```{note}
  It is up to the upper layers to provide reliability. IP nor UDP do it, so unless the application layer provides it, we can only rely on TCP to get a frame restransmitted.
  ```

### Ethernet addresses

The Ethernet protocol defines 6 byte long (48 bits). They are represented as 6 bytes in hexadecimal separated by colons.
These addresses are associated to the NICs (_network interface controller_) attached to the node.
Each interface has its own MAC address. That way, a node can have multiple NICs attached to it each of them with a different MAC address.
The MAC address identifies the NIC in a particular LAN.

The structure of a MAC address can be divided in 2 groups:

- The _organisationally unique identifier_ (OUI): the first 3 bytes, that identifies a specific manufacturer.
  IEEE assigns them.
  When an OUI is used, then the last 2 bits of the first byte will be always `00`.
  All addresses using an OUI will be _globally unique_.
  If an administrator replaces the OUI and uses a _locally unique_ identifier, then it is expected that these bits are `10`.
- The _NIC specific_: the last 3 bytes.

When a MAC address is used as destination address, the last bit of the first byte determines the type of the frame:
- _Unicast_: if the last bit is 0.
- _Multicast_: if the last bit is 1. A _broadcast_ frame is really a special case of a multicast one as all bytes are set to `FF`.


The MAC addresses are written as 6 bytes separated by colons.
However, they are _not_ transmitted like that.
Instead, each byte is transmitted in the reversed order so the LSB of each byte is sent first.
This is why the last bits of the first byte contains the type of the frame: _they are transmitted and received first_.

```{note}
Important to note: even though a frame is unicast, that does not mean that, in a _shared medium_ the frame is only received by the destination.
In a shared medium like a bridged cable LAN or a WLAN environment, _all_ nodes will receive the unicast frame.
However, only the affected node will reply to it.
```

### Ethernet MAC layer

The MAC sublayer of Ethernet provides a way to access to a _shared medium_.
Shared media are problematic:

- Multiple nodes want to transmit at the same time. It requires a way to provide access to the transmission media in turn.
- Collisions: when 2 or more nodes transmit at the same time a _collision_ is produced.
  This degrade the media utilisation, waste resources and increases the delay during communcation.

The solution to this problem proposed by Ethernet is to use a technique called _carrier sense multiple access with collision detection_ (CSMA/CD).
This mechanism to avoid collisions work as follows:

1. Nodes listen to the channel before start transmitting.
1. If it is used, then wait for a certain time.
1. If not used, then transmit and listen for other frames coming in.
   If you can only see your message, then OK. If not, then abort the transmission and as a collision has been detected.
   The frame will need to be resent again.

### Ethernet frame

The standard Ethernet frame size goes from 64 to 1518 bytes. It can carry from 46 to 1500 bytes of data:

- _Preamble_: 8 bytes that is not counted as part of the frame legnth.
  The preamble is made of 8 bytes:
  1. First 7 bytes are `10101010` (55 decimal).
  1. Last byte is the _start frame delimiter_ (SFD) and it is `10101011` (213).
- _Target address_: 6 bytes.
- _Source address_: 6 bytes.
- _Type_: 2 bytes defined by the IANA:
  1. From 0 to 45 are invalid values.
  1. From 46 to 1500 are reserved to encapsulate LLC frames (802.2).
	 _In this case, the field indicates the length of the data field and not just the type_.
  1. From 1500+ uses values assigned by the IANA to define the type of the protocol encapsulated.
	 For example `0x8000` is IPv4.
- _Data_: from 46 to 1500 bytes. If the data is lower than 46, then it is fill with 0s.
- _Frame check sequence_: the CRC for detecting transmission errors.

It is interesting that, if the `type` field value is between 46 and 1500, this field actually tells the length of the data field because it will carry an LLC frame encapsulated in it.
These frames are useful for supporting upper layers protocols that:
- Protocols that do not have a length field for the data.
- Protocols that use flow control features like NetBIOS.
- Protocols that require the _subnetwork access protocol_ (SNAP header) since they used private protocol identifiers.

In these situations, the LLC frame is the one carrying the data and because of some extra headers introduced by LLC, the minium and maximum data that they can carry changes from 46-1500 to 38-1492 (8 bytes less).

## ARP

```{note}
Now it is time to revisit the encapsulation process from top (application) to bottom (data-link).
Whatever message we generate at the application layer, we will have to send no less than 64 bytes at the link layer (14B of header and 46B of data encapsulating multiple and 4B as tail).
This means that if the application layer generates 4 bytes of data, it will fit in this minimal frame size.
Note that if not, the data will be filled with 0s.
```

```{note}
Let's suppose our PC sends an HTTP request to a web server:

1. The PC generates the message with the right source and destination IP addresses and, based in its routing table, it is sent to its gateway.
1. The router analyses the destination IP and, based in its routing table, forward the IP packet to its next hop.
1. The second router analyses the destination IP and, based in its routing table, locally delivers the packet to the web server.

The local delivery performed in the first and last step is performed within the same network, at link level.
There must be a mechanism that transforms the destination IPs to the actual MAC addresses of the devices.
```

_Address resolution protocol_ (ARP) is a neighbour discovery protocol that helps with the problem of getting the MAC address given an IP address.
When a node needs the MAC address of a given IP for delivering a frame to a local neighbour it sends a broadcast request.
The answers are stored in a cache for future use.

```{note}
The ARP cache can be managed using `arp` and `ip neigh` commands:

:::
$ ip neigh
192.168.223.238 dev wlp0s20f3 lladdr 11:22:33:44:55:66 REACHABLE
172.17.0.2 dev docker0 lladdr 01:02:03:04:05:06 STALE

$ sudo ip neigh add 192.168.1.1 lladdr 66:11:66:11:66:11 dev wlp0s20f3

$ ip neigh
192.168.223.238 dev wlp0s20f3 lladdr 11:22:33:44:55:66 REACHABLE
192.168.1.1 dev wlp0s20f3 lladdr 66:11:66:11:66:11 PERMANENT
172.17.0.2 dev docker0 lladdr 01:02:03:04:05:06 STALE

$ sudo ip neigh del 192.168.1.1 dev wlp0s20f3
:::
```

1. The _ARP request_ is broadcasted to all the nodes. The request is for discovering the MAC address of a certain IP.
1. The _ARP reply_ is unicast, from the node that has the matched IP. It includes its MAC address.

The ARP message is encapsulated in an Ethernet frame of type `0x0806` and has the following structure:

- _HW type_: 2 bytes. Tells the type of the link layer protocol. For Ethernet `0x0001` is used.
- _Network type_: 2 bytes. Tells the type of the network layer protocol. For IP `0x0800` is used.
- _HW len_: 1 byte. The length of the link-layer addresses. `0x06` for Ethernet.
- _Protocol len_: 1 byte. The length of the network-layer addresses. `0x04` for IP.
- _Operation type_: 2 bytes. The ARP operation. `0x0001` for request or `0x0002` for replies.
- _Sender HW address_: variable length.
- _Sender Network address_: variable length.
- _Target HW address_: variable length.
- _Target Network address_: variable length.


```{note}
In the example, node A wants to know the MAC address of B. It sends an ARP requests (the example needs to be read from the right to the left):
- The frame's detination address is the broadcast: `FF:FF:FF:FF:FF:FF`.
- The frame's type is ARP (`0x0806`).
- The data in the frame is an ARP message with the following content:
  - HW type and network type sets to Ethernet and IP. (there is a mistake in the slide: it is `0x0001` not `0x0002`)
  - HW len and protocol len are set to 6 and 4 because of the length of the Ethernet and IP addresses.
  - The operation type is `0x0001` for a request.
  - The sender's addresses are filled accordingly.
  - The target HW address is set to `00:00:00:00:00:00` as it is unkown

B replies with a unicast ARP reply and it contains its IP address (as part of the sender's protocol address).
```

## Bridges and Switches

As we have seen before, connecting multiple devices requires sharing a transmission medium.
That is problematic in many cases because of collisions.
The use of CSMA/CD (and other techniques) reduces the chance of collisions.
However, collisions may still happen and that reduces the utilisation of the channel.

Ethernet has evolved to provide better performance and in its earlier stages used _bridges_ (also known as _hubs_) to connect multiple hosts and reduce the amount of collisions.
_Switches_ were introduced later as an improvement of bridges to avoid collisions even further.

### Bridges

Bridges (hubs) are used to split a collision domain in multiple ones.
They forward the frames coming from one collision domain (connected to one of the bridge _port_) to the other ones (connected to the rest of the ports).

```{note}
Let's suppose the 2 port hub of the slide:
1. A frame coming from the left side is forwarded to the right side to _all_ hosts.
1. Only the target host generates a reponse and send the frame back to the left side.
1. The bridge forward the response to _all_ the nodes at the left side.
1. Again, only the target host processes the response.
```

By separating the collision domains, bridges improve the bandwidth of the shared medium.
For example, 6 nodes connected to a shared medium of `10Mbps` would have `10/6 = 1.6Mbps`.
Adding a bridge of 2 ports, the collision domains can be split in 2, so each domain will have 3 hosts.
Now, the bandwidth will be `10 / (3 + 1)` (as we should count the bridge itself too) which is `2.5Mbps`.

Bridges are not smart enough for _filtering_. In fact, they are physical-layer devices. They do not have any knowledge of

### Switches
