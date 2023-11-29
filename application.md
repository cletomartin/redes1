(application)=
# Application layer

This lesson describes in depth the application layer and describes multiple application-layer protocols.
You can find the slides [here](slides/application.odp).

As it has already mentioned in the [architecture](arch) chapter,
the each protocol layer provides a certain service to the upper-level layer and requires functionality from the lower one.
In this case, the application layer is at the top of the stack so:

1. It _provides_ service to the user: from the user point of view, there is a _logical connection_ between its application and the remote one as they were directly connected sharing messages.
   Obviously, this connection is actually performed by the lower-level layers down to the physical layer.
1. It _uses_ the transport layer to send its _messages_: depending on the selected transport protocol the message deliveries could be guaranteed or not.

There are _public-domain_ protocols, defined in RFCs, like HTTP or DNS, and _proprietary_ protocols like Skype or WhatsApp.
Since the public-domain ones are standardised and publicly available they are typically adopted for a better interoperability between different manufacturers.

The application-level protocol defines mainly the following features:

- **Messages**: the valid syntax and structure of messages (fields and values), the meaning of the messages (semantics), and the types of messages (e.g. requests, reponses, control, etc.)
- **Message processing**: those rules about how and when messages should be processed.

## Paradigms

The application layer communicates two or more applications.
The role of the applications that take during the data exchange defines the _paradigm_ of the communication.
There are 3 paradigms:

1. **Client-Server**: this is the most traditional one where the client contacts the server which is always on-line waiting for clients to connect.
   The client _initiates the connection_ to server in order to perform a _request_ and the server replies to that operation with a _response_:
   - Multiple clients can connect to the same server.
   - Clients cannot connect directly to each other.
   - The server has to be always reachable by clients.

   Applications using this paradigm usually provides 2 different programs: the client application and the server application.

1. **Peer-to-Peer**: the main problem with the client-server paradigm is that the server side becomes a _single-point-of-failure_ (SPOF) and it often needs to be replicated.
   This replication might not be easy to implement in some cases.

   The alternative paradigm is to have a network of _peers_, i.e. nodes that can _request_ and _response_ messages.
   This means that:
   - There is not a central entity that needs to be always available.
   - The system can grow just by adding nodes to the network but they are difficult to manage and control.

   P2P systems are used in some limited context.

1. **Mixed**: some applications used both client-server and P2P paradigms at the same time, depending of the operation they are performing.
   For example, the lookup operations of available peers can be done with a client-server approach whereas the connection between peers would be done via P2P.

## Transport requirements

TBD

## Implementation example

A basic way to implement applications that require communication is using _sockets_ which is a facility provided by the operating system for sending and receiving data using by using the transport layer.
The developer can choose what type of transport layer to use and many other parameters of the communication.

```{note}
You can show a trivial [client](src/client-server/client.py) and [server](src/client-server/server.py) applications.
Students do not need to understand everything, just the overall process and get in contact with the concept of socket.

Firstly run:

:::
python server.py
:::

And in a different terminal:

:::
python client.py
:::
```

## Web and HTTP

## HTTPS

## SSH

## DNS

## P2P
