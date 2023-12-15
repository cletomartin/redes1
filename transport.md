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

In general, the process of delivery might happen in 2 ways:

- _Push_: the sender produces the data as it is

### Error control

### Connectionless and connection-oriented protocols

## Transport-layer protocols in TCP/IP suite

### UDP

### TCP

## Reliable protocols

### Simple protocol

### Stop and wait

### Go back N

## Exercises

> TBD
