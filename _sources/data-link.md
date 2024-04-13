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
- The _media access control_ (MAC): similat to our already known MAC.

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


## ARP

## Bridges and Switchers

## Networking examples
