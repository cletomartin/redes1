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

It is important to control the amount of data a sender can _produce_ and a reciever can _consume_.
There needs to be a _balance_ between them:

- If the sender produces too few data, the reciever might be idle.
- If the sender produces too much data, the reciever can be overwhelmed.
- Circunstances might change as communication progresses (e.g. the receiver might get slower because of it is busy with something else).

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

- _Between the receiver's transport layer and the receiver application_: the reciever application _pulls_ data from the its transport layer.
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
  They are individual packets that the reciever will treat as separated units.
  The datagrams are sent in order but the transport layer _will not_ guarantee that the packets arrive in order to the application or prevent their loss.

  This type of transport-layer protocols just provide a simple mechanism of sending packets from one application to another, without really providing extra services.
  This is the case of UDP.

  ```{note}
  In the example, the packets arrive out of order and they are passed to the receiver's application as they arrive, without any flwo or error control
  ```

- _Connection-oriented_: the data is sent through a _logical connection_ between the sender and reciever.
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

The User Datagram Protocol (UDP) is the _conectionless_ transport protocol included in the TCP/IP protocol suite.
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
    1. A _pseudoheader_ of source IP, destination IP, protocol type and UDP length.
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

## Reliable protocols

### Simple protocol

### Stop and wait

### Go back N

## Exercises

> TBD
