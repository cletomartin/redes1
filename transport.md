# Transport layer

This lesson describes in depth the transport layer and describes some protocols for reliable data transmission.
You can find the slides [here](slides/transport.odp).

The transport layer provides a way to communicate _processes_ that are located in different places.
These means that two applications can send and receive messages as they were directly connected.
The transport layer uses the network layer to transmit information between hosts.

```{note}
It is important to remark the difference between the transport and network layer: the network layer's domain is the hosts whereas the transport layer's domain is the processes (applications) that run on these hosts.
```

In this section we are going to study the services provided by the transport layer to the application layer.

## Services

In this section some general concepts and transport-layer services are described.
These services are provided to the application layer.

### Port addressing and sockets

As it has been already mentioned, the transport layer communicates processes running on hosts.
Because an application could send data to one or more applications on another host, some kind of process addressing would be required.
The transport layer uses _port numbers_ for distinguish applications within a server.

Using the client-server paradigm:

- A server application uses a _fixed_ port so all clients can contact to it.
  It is usually said that _an application is listening on port X_ to describe
- A client application uses an _ephemeral_ port: its existence only lasts while communication takes place and can be changed the next time.

Although we have not get into the [network layer](network), every hosts has its own network address (usually an IP address).
The port number is a _higher-level_ address as it points to an application running on the host:

- The IP address selects the host.
- The port number selects the application of the host.

The combination of IP address + port number is known as _socket address_.

```{note}
This is what we used in our example of socket programming: `s.connect((HOST, PORT))`.
```

The standard organisation ICANN has defined the following port ranges:

| Name       | Range       | Description                           |
|------------|-------------|---------------------------------------|
| Well-known | 0-1023      | Controlled by IANA                    |
| Registered | 1024-49151  | Registered by IANA but not controlled |
| Dynamic    | 49152-65535 | Temporary and private ports           |

```{note}
Explore `/etc/services` and show the different applications associated with the port numbers.
Also mention that there can be 2 ports for a speific applications (TCP and UDP).
```

```{note}
Explain the example of using `nc` for creating a local TCP server and listen on port 12345.
With `netstat` you can explore the processes that are currently listening:

- `-l`: shows only those processes in `LISTEN` status.
- `-p`: shows the program names.
- `-t`: shows only TCP.
- `-n`: shows IPs instead of hostnames.
```

### Encapsulation and decapsulation

As any intermediate layer, the transport layer receives messages from the application layer and from the network layer:

- _Encapsulation_: application messages are transformed into _segments_ or _datagrams_ (depending on the transport protocol we use).
  The application message (the _payload_) is appended with a _transport header_ that describes its content and has useful information for the receiver to consume.
  This process happens on the _sender_ side.

- _Decapsulation_: the transport layer processes each segments or datagrams coming from the network layer.
  It removes the transport header and passes the payload to the application network.
  This process happens on the _receiver_ side.

### Multiplexing and demultiplexing

Multiple processes can be communicating all at the same time, exchanging information with different remote processes.
The transport layer needs to be able to perform the following operations in order to achieve this:

- _Multiplexing_: _many_ processes will use the transport layer as _one_ logical channel.
  This is performed at the sender side.
- _Demultiplexing_: the information that comes from the transport layer's logical channel needs to be deliver to the right process.
  This is performed at the receiver side.

### Flow control

It is important to control the amount of data a sender can _produce_ and a receiver can _consume_.
There needs to be a _balance_ between them:

- If the sender produces too few data, the receiver might be idle.
- If the sender produces too much data, the receiver can be overwhelmed.
- Circumstances might change as communication progresses (e.g. the receiver might get slower because of it is busy with something else).

In general, a process may deliver data in 2 ways:

- _Pull_: the receiver _requests_ for more data to the sender.
  In this case, there is no need of flow control mechanism as the receiver can request data as needed.

- _Push_: the sender delivers the data _as it is produced_.
  This mechanism requires some kind of control as the receiver can be overwhelmed or being idle.

This pull and push model is used differently across the components of the transport layer:

- _Between the sender application and the transport layer_: the application _pushes_ data to the transport layer,
  so there is a flow control mechanism between them.

- _Between the sender's transport layer and the receiver's transport layer_: when segments/datagrams are ready, the sender's transport layer _pushes_ them to the receiver's one.
  Another flow control mechanism is needed here too.

- _Between the receiver's transport layer and the receiver application_: the receiver application _pulls_ data from the its transport layer.
  In this case, a flow control mechanism is not required as the application consumes data on-demand.

The transport layer provides this flow control mechanism as we will see by the end of this chapter.

### Error control

The transport layer might work on top of an _unreliable network layer_. That's the case, for example, for the TCP/IP stack.
For this reason, the transport layer provides a way to detect errors of the data transmitted.
Specifically, it has to deal with:

1. _Corruption detection_:data might be modified during their trip across the network.
   The transport layer provides a mechanism for detecting this type of data and discard them.
1. _Loss detection_: data packets might be lost so the transport layer will provide a way to detect this loss and request for being resent.
1. _Duplicate detection_: data packets might arrive duplicated for multiple reasons so the transport layer will discard any duplicated packet.
1. _Out-of-order detection_: data packets might arrive in different order due to network conditions so the transport layer will detect it and re-order them properly.

All these are achieved using these mechanisms:

- _Checksums_: numerical values generated from the sent data. They can be used by the receiver for checking that the data haven't been altered.
- _Sequence numbers_: packets are tagged with a increasing number so the order can be checked by the receiver.
- _Acknowledgement_: when packets are received, the receiver will have to acknowledge its arrival to the sender.
  Thus, the sender knows which packets arrived and which ones did not.
- _Timers_: as the network is not reliable, sender and receiver will use different timers that will expire if data are not acknowledged on time or expected replies never arrive.

### Congestion control

Congestion may happen on any system shared by different users that try to make use of it at the same time.
A congested network is a network where nodes _need to wait_ for transmitting data.

The networking nodes (e.g. routers) use queues internally for dispatching packets to different routes.
These queues can be full if the networking nodes cannot consume packets at higher rate than they arrive.
The problem usually happens at network level and it manifests at transport layer too.


### Connectionless and connection-oriented protocols

Since the transport layer might work on different context and applications,
it is possible that not all features might be required because another layer is already providing them or they are not required for a particular context.
For these reason, the transport layer might be:

- _Connectionless_: the data is sent in _atomic chunks_. These chunks, known as _datagrams_, do not have any kind of relationship between each other.
  They are individual packets that the receiver will treat as separated units.
  The datagrams are sent in order but the transport layer _will not_ guarantee that the packets arrive in order to the application or prevent their loss.

  This type of transport-layer protocols just provide a simple mechanism of sending packets from one application to another, without really providing extra services.
  This is the case of UDP.

  ```{note}
  In the example, the packets arrive out of order and they are passed to the receiver's application as they arrive, without any flwo or error control
  ```

- _Connection-oriented_: the data is sent through a _logical connection_ between the sender and receiver.
  The connection should be _established_ before sending data and has to be _closed_ afterwards.
  The packets transported through a specific connection are related each other: they belong to the same context of communication.

  This type of transport-layer protocols provide a more sophisticated set of services and can be used over unreliable layers like the network layer as
  flow and error controls are implemented.
  This is the case of TCP.

## Transport-layer protocols in TCP/IP suite

TCP/IP protocol stack defines 3 transport protocols that can be used:

- UDP: User Datagram Procotol (connectionless)
- TCP: Transmission Control Protocol (connection-oriented)
- SCTP: Stream Control Transmission Protocol (connection-oriented that supports multiple redundant paths).

We are going to focus on UDP and TCP. SCTP offers more complex services than TCP and it is used only in few context.

### UDP

The User Datagram Protocol (UDP) is the _connectionless_ transport protocol included in the TCP/IP protocol suite.
It should be consider _unreliable_ so it is up to the application layer to provide reliability if it is required.
This protocol is useful when a minimal overhead is required (e.g. real-time applications) and reliability/control is not strongly required (e.g. video/audio transmission).

UDP uses _user datagrams_ (or just _datagrams_) as packets.
It has a fixed header of 8 bytes:

- 2 bytes for the _source port_.
- 2 bytes for the _destination port_.
- 2 bytes for the _total length_ of the data.
  This means that a datagram can carry up-to 64KB ($2^{16}$ bytes).
- 2 bytes for an _optional checksum_:
  - If checksum is not desired, then it will be filled with 0s.
  - Checksum is calculated by adding all together in chunks of 16-bits the following:
    1. A _pseudo-header_ of source IP, destination IP, protocol type and UDP length.
	1. The UDP header.
	1. The UDP data.

In essence, UDP provides no more than process-to-process communication on top of of the network layer:

- It is connectionless.
- No flow control.
- No error control although the optional checksum might be used by the application layer.
- No congestion control.

When an application requires a UDP port, the operating system creates 2 queues: _incoming_ and _outgoing_.

```{note}
Show some of the well-known UDP protocols.

In Debian, you can install `inetsim` which includes many fake servers for different UDP protocols:

:::
sudo apt install inetsim
:::

Make sure that the Echo UDP service is running:

:::
sudo service  inetsim status | grep echo
:::

In one terminal, you can show the log of `inetsim` so people can see the actions taken by each server:

:::
sudo tail -f  /var/log/inetsim/service.log
:::

Then you can use the following to show it working:

:::
$ nc -u 127.0.0.1 7
Hello!
Hello!
:::

Another interesting example is Daytime.
Show [RFC867](https://datatracker.ietf.org/doc/html/rfc867) at UDP datagram.
You can run the following:

:::
$ nc -u 127.0.0.1 13
type whatever
Sat Dec 16 16:15:40 2023
:::

Also show the [DNS example](src/simple-dns/main.py).
Just run it with:

:::
$ python src/simple-dns/main.py
:::
```

### TCP

The Transmission Control Protocol (TCP) is a _connection-oriented_ protocol that provides a reliable packet transport to the application layer:

- It is based on a combination of _Go Back N_ and _Selective-Repeat_algorithms.
  Lost and corrupted packets are retransmitted.
- It uses mandatory _checksums_ for error control.
- Use of control messages like ACKs for ensuring packets are received.

TCP is a complex protocol where client _establishes a connection_ before exchanging data with the server.
At the end of the communication, the connection is closed.

TCP can be described as a _Finate State Machine_ (FSM).
The machine is really a program receiving/sending data and jumping between states.
The next state will depend on:
- The information received
- The specific state where the machine is in.

```{note}
Show the state diagram.
The machine starts in `LISTEN` state. In that state, if a `SYN` message is sent, the machine changes to `SYN_SENT` state.
```

TCP provides a _stream delivery service_.
This means that the information is transmitted as a stream of bytes from the client to the server.
From the client and server points of view, there is an imaginary pipe _connected_ to both ends where bytes arrive in order to the other side.

TCP packets are called _segments_ and the segments of a specific connection are related each other.
This means that the fields in the headers are logically connected to previous and following segments so they can be reassembled when received.

```{note}
We will see this more in depth in the following sections but it is worth mention the _circular buffers_.
This technique is used by TCP for providing reliability and flow control:

- On the sender side, they keep two types of segments:
  1. The ones ready to be sent: these segments are built straighaway from the data coming from the application layer.
  1. The ones already sent: when segments are already sent, the buffer can rotate and move on.

- On the receirver side, they keep two types of segments:
  1. The ones just received but not read: those are waiting to be read by the applicatio.
  1. The ones read by the application: when segments are read, the buffer can rotate and move on.
```

One of the important header fields are the _sequence number_ and the _acknowledgement number_.
They both define the _numbering system_ of TCP that allows:
- Reliability: as they provide confirmation of the reception.
- Flow control: they define the amount of data the receiver is able to digest.

TCP assigns numbers to the data. This _byte number_ is:
- Different for each direction of the communication.
- Initially generated randomly. It does not need to correlate to the data that is meant to be sent.

  ```{note}
  For example: we want to sent 6000 bytes of data.
  If the first byte is numbered as 5432 (generated randomly) the last byte will be $5432 + 6000 - 1 = 11431$
  ```

TCP also assigns numbers to each segment. This is known as _sequence number_ and it is generated as follows:

- The _initial sequence number_ (ISN) for the first segment is generated randomly. It will be typically the first byte number (also generated randomly).
- The following sequence number will be the previous segment's sequence number plus the number of bytes carried by this previous segment.

   ```{note}
   The example of the slide is the transmission of a file of 5000 bytes in 5 segments.
   If the first byte was labeled as 10001, the:
   - The first sequence segment will be 10001 and it will contain 1000 bytes.
     The range of the byte numbers will be from 10001 to $10001 + 1000 - 1 = 11000$
   ```

  TCP segments can carry data and/or control information. Sequence numbers are _only_ use when data is carried.
  For those segments that only carries control information, the meaning of their sequence number is different: they are not related with the data transmission.
  As we will see later, for the future sequence numbers, these segments just consume 1 sequence number (as the carried 1 byte).

On top of the sequence number, TCP header can also include an _acknowledgement number_.
The value of this number is the next byte number of the last one received.
In other words, _it is the number of the next byte expected_.
For example: if `ack = 5643` it means that all bytes until `5642` has been recieved and we are waiting for the next one.
Of course, it does _not_ mean the total bytes received are 5642 because the initial byte number is random and it is likely it was not 0.

#### The TCP segment

A segment has two parts:

- A header that can be between 20-60 bytes.
- The payload of the TCP segment.

The TCP header has the following structure:

- _Source port address_
- _Destination port address_
- _Sequence number_: if needed, it is the value of the first byte number carried by the segment.
  Initially it takes a random ISN as value.
- _Acknowledgement number_: if needed, it is the value of the byte number expected.
  The previous byte number has been received properly.
- _Header length_: measured in 4-byte words. This field is 4-bit long and since the header can be from 20 to 60 bytes, the values of this field might be from 5 to 15.
- _Control bits_: a 6-bit field where each bit categorise the segment:
  - `URG`: the segment carries urgent data so the urgent pointer field is valid.
  - `ACK`: the segment is an acknowledgement.
  - `PSH`: the segment data should be pushed to the reciever application without waiting for buffers or windows.
  - `RST`: the segment requires the connection to be reset.
  - `SYN`: the segment requests the synchronisation of sequence numbers.
  - `FIN`: the segment requests the termination of the connection.
- _Window size_: gives the information to the sender of the the maximum amount of data that the receiver wants to receive.
  Thus, the sender will have to respect this value.
- _Checksum_: it is mandatory in TCP and it is calculated very similarly to UDP's one (it adds the pseudo-header on top of the TCP segment).
- _Urgent pointer_: if `URG` was set, this field points to the last byte of the urgent data within the segment.
  The urgent data is placed at the beginning and this pointer helps to know when it ends.
- _Options and padding_: this optional field might incorporate extra data up to 40 bytes.


#### The TCP connection establishment

TCP is a connection-oriented protocol where a _bidirectional connection_ is established between sender and reciever before any data is exchanged.
Once this connection is established, all segments will be logically related to this connection.

The TCP connection establishment is known as the _three-way handshaking_ and it works like this (values come from the example of the slides):

1. The server starts to listen for incoming connections.
   We say the server has a _passive_ role during connection openings because it waits for the client to start them.

1. The client starts creation of a connection to the server.
   We say the client has an _active_ role during connection openings because it initiates them.

   The first one is `SYN` segment which requires to the server to synchronise the sequence numbers.
   The _ISN_ in the example is 8000.

1. The server receives the `SYN`, so it sends a segment of 2 types:
   - `SYN`: requesting the client to synchronise the sequence number. The server's ISN is 15000.
   - `ACK`: acknowledging the previous client's `SYN`. So the `ACK` number is 8001.

1. The server recieves the `SYN-ACK` segment and responses with an `ACK` segment.
   This segment acknowledges the `SYN` request in the previous message so:
   - The sequence number is 8001 as it is the following one to 8000.
   - The `ACK` number is 15001 since we have recieved 15000 before.

   ```{tip}
   The client could also send data along this `ACK` segment.
   That way it can take advantage of this `ACK` segment and start sending data instead of doing it in a different segment.
   This is known as _piggy-backing_.
   If the client does _not_ piggyback data within this segment, the sequence number will _not_ be increased later.
   ```

1. The connection is now established.

This connection establishment procedure has an intrinsic problem: the server has to acknowledge the initial `SYN` sent by the client.
A malicious actor can send lots of `SYN` segments with _spoofed_ source IP.
This will make the server to send lots of `SYN-ACK` segments to clients that do not exist.
Since they do not exist, the server will never get a response so it will wait for the `ACK` untile the timeout expires.
If there are lots of `SYN` segments it is possible that the server waits for so many clients that it reaches its limit.
Thus, any _new and legit_ `SYN` request will not be replied. This is a classic _Denial of Service_ (DoS) attack.

#### The TCP data transfer

Once the connection is established, then the bidirectional data exchange can happen:

1. The client sends 1000 bytes:
   - The `SEQ` number is again 8001 because the previous `ACK` (the last segment of the connection establishment) did not contain data.
   - The `ACK` number is again 15001 because it is the expected byte number from the server.
   - The `PSH` is on.
   - Note the byte numbers go from 8001 to 9000

1. The client sends another 1000 bytes:
   - The `SEQ` number is now 9001 (8001 + 1000).
   - The `ACK` is still 15001
   - The `PSH` is on.
   - The byte numbers go from 9001 to 10000

1. The server has recieved both segments and it replies with an `ACK` segment piggybacked with data:
   - The `SEQ` number is 15001.
     It is still the same sequence number as the server has not sent data until now.
   - The `ACK` number is 10001, meaning that both chunks of 1000 bytes have been received.
   - The `rwnd` is set to 3000, telling the client not to send more than 3000 bytes in a segment.
   - 2000 bytes of data, so the byte numbers will go from 15001 to 17000.

1. The client recieves the segment and creates another `ACK` segment, this time with no data:

   - The `SEQ` number is 10001, as it comes after 1000 bytes previously sent.
   - The `ACK` is 17001, telling the server that it has recieved the last 2000 bytes.
   - The `rwnd` is set to 10000, telling the server not to send more than 10000 bytes in a segment.


#### The TCP connection termination

After the data is exchanged, the connection can be terminated at any time.
The closure can be done in 2 ways:

- _Three-way handshaking_: this will fully terminate the connection.
- _Half-close_: this will allow the server to send data to the client before closing the connection.


The three-way handshaking connection termination is as follows:

1. The client sends a `FIN` segment. The `SEQ` and `ACK` number values would depend on the previous conversation, so let's suppose `x` and `y`.

   ```{tip}
   This `FIN` segment may also piggyback data, in which case it will affect the following sequence numbers.
   ```
1. The server sends a `FIN-ACK` segment, acknowledging the previous `FIN` request.
1. Finally, the client sends an `ACK` segment previous server's `FIN` segment.

The half-close connection termination is as follows:

1. The client sends the `FIN` segment.
1. The server sends an `ACK` segment this time, meaning that the `FIN` has been recieved..
   However, the server still can send data to the client as a `FIN` was not sent.
   All the recieved data in this time period will be acknowledged by the client.

1. When the server finishes the sending data, its `SEQ` number would be `z`, so a `FIN` is sent to the client with this sequence number.
1. Finally, the client sends an `ACK` segment for `z + 1`.


### Segment loss

In a normal operation, `ACK` numbers are always recieved in order.

```{note}
In the example, a client and a server exchange data:

- 200 bytes to the server
- 1000 bytes to the client
- Client acknowledges.
- Server sends 2 segments of 1000 bytes each.
- Client acknowledges both.
```

However, some segments might get lost. This is detected because client and server keep a set timers and, if the expire, segments are retransmitted.

```{note}
In the example, a client and a server exchange data:

- The client sends 2 segments of 100 bytes each.
- The server acknowledges both.
- The client sends another 2 segments of 100 bytes each but the first one is lost.
- The server sends `701` as `ACK` number because, even though it has recieved the second chunk, the first one was not.
- The client's timer expired for the chunk 701, so the segment is re-sent.
- The server now recieves it so it can now acknowledge both (701 and 901).
```

## Reliable protocols

As we have mentioned, TCP is a complex protocol that uses different techniques for achieving flow, error and congestion control.
In this section we are going to explore some of the protocols that provide reliability.

### Simple protocol

The simplest protocol that provides reliability is the one that works on ideal conditions:

- No packet is lost.
- There is no corrupted packets along the way.
- All packets arrive in order.

Under this cirscunstancies, the protocol can be connectionless and there is no need of flow/error/congestion control.
However these are ideal conditions that almost never happen in reality.

### Stop and wait

This protocol is the simplest way to provide flow and error control to an unreliable network.
It uses a _sliding window_ of size 1, which means that the sender has to wait for the ACK of a packet before sending a new one.
With this simple approach, the flow control is provided (the reciever only sends the ACK when it is ready to receive more).

In this protocol, the following mechanisms are used:

- _ACK for each packet_: which means a sliding window of size 1.

- _Sequence numbers_: the amount of sequence numbers depends on the size of the sliding window.
  It uses $mod 2^{m}$. This is the same as saying that it goes from 0 to $2^{m}-1$.
  In this case, the sequence numbers will be 0 and 1.

- _Checksum_.
- _Timers_: for each packet sent. If no ACK is recieved and timeout expires the packet will be retransmitted.

In general, the sliding window size $N$ depends of a variable $m$: $N = 2^{m}-1$.
The top and wait protocol uses $m=1$, so the window size is $2^{1}-1 = 1$.
The window size can be seen as the buffer that controls what has been sent or recieved.

```{note}
In the diagram, you should show that window size is the sum of:
- Packets already sent but not ACK'd
- Packets ready to be sent.

When an `ACK` is recieved, the window slides the amount of positions that the `ACK` includes.
```

```{note}
The example flow diagram works like this.:

1. Since we are in stop and wait protocol, both sender and receiver use $m=1$ so both have a window size of length 1. The sequence numbers are 0 or 1.
1. The sender starts sending the packet 0. It starts a timer associated to this packet.
1. The receiver moves its window one position and sends an `ACK`. Note that `ACK 1` confirms the reception of packet 0.
1. The sender gets the ACK and moves its window one position further. The timer is stopped.
1. The sender sends the packet 1. It starts a timer again.
1. The packet 1 gets lost.
1. Since nothing happens, the timer expires.
1. The sender resend the packet 1.
1. The receiver gets packet 1, move its window one position forward and sends the ACK.
1. The sender receives the ACK and moves its window one position ahead. The time is stopped now.
1. The sender tries to send packet 0 now.
1. The receiver gets it and moves its window one position more. Note that the receiver now waits for packet 1, so it sends `ACK 1`.
1. The ACK 1 gets lost.
1. Since the sender did not get any ACK, it resends packet 0.
1. The receiver gets packet 0 but it is wainting for packet 1, so it discards it considering it as duplicated.
```

### Go back N

## Exercises

> TBD
