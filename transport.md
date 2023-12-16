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

### TCP

## Reliable protocols

### Simple protocol

### Stop and wait

### Go back N

## Exercises

> TBD
