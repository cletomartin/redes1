(archs)=
# Network architecture

This lesson introduces the concept of protocol layering, showing ISO and TCP/IP models.
You can find the slides [here](slides/architecture.odp).

## Introduction
A network architecture describes how a network is organised, its components and its _protocols_ or communication rule set.

When the communication is simple we may need a simple _protocol_ to reach an effective exchange of information between peers.
However, automating this communication is usually a complex process that requires the implementation of specific rules (protocols) in order to be achieved.
In fact, even a simple human conversation can have hidden complexity underneath:

- They should talk a language that both can understand.
- They should respect the other's turn before talking.
- It is expected to follow good manners. For example, say hello, ask for things kindly, farewell before leaving, etc.

This examples gets even more complicated if we introduce new variables:

- The speakers do not share a common language so they need some translation mechanism.
- The speakers are located apart from one another.

If we want to deal with complex communication problems, we will have to divide each problem into simpler functions or tasks that will collaborate each other in order to get the overall communication done.
This is an intuitive idea of _protocol layering_:
divide the communication problem into different phases which solve _a particular issue/problem_ of the overall communication process and _delegate_ the rest to other phases to other layers.

```{note}
The Philosopher's analogy is an illustrative example. See that each layer of the communication use a information useful at its own level.
For example, the translator has a field called `L` for the language and the sender uses the fax number.
```

Protocol layering organises the communication mechanism in layers that:
- Are sorted by _abstraction level_, from the end user to the transmission medium.
- Require functionality from upper layers and provide it to the lower ones.
- At both ends, each layer can be seen as they maintain a virtual conversation that makes sense at the layer's level.

```{note}
Two principles of protocol layering:

1. Each layer should be able to perform two opposite tasks: for example send/receive, or encrypt/decrypt.
1. Each layer should share the same object at both ends of the communication. For example, an encryption layer should have a chiphertext at both ends.
```

## Reference models

In this section two main reference protocol models are shown. They describe how different protocol layers can cooperate so a computer network can be implemented.
Depending of the defined details, the model can be _more specific_ by describing the detailed behaviour of each layer and the protocols used,
or it can be _more general_ defining the model conceptually.

### OSI

The Open System Interconnection (OSI) model is a reference model created by the ISO by the late 1970s. This is a general and conceptual model that can be used for describing other computer communication models too.

This model defines 3 key components for each layer:

1. **Service**: the functionality that a layer provides.
1. **Interface**: the mechanism on how to get the service from a layer.
1. **Protocol**: the communication rule set between the communication ends of a layer.

From bottom to top, the layers of this model are:

1. **Physical**: it is in charged of transforming bits into electrical/mechanical signals and its reverse operation.
   This layer is very dependant of the transmission medium. Both ends of this layer send and receive _bits_.
1. **Data link**: provides data transmission between nodes that are directly connected (cable, air, etc.).
   The data transmission is grouped in set of bytes called _frames_.
   At this level nodes need to have some addressing mechanism and a common one, used in multiple types of networks, is the _Media Access Control_ (MAC) address.
1. **Network**: provides data transmission between nodes that are not directly connected.
   At this level, a source node can send data to a target node and some intermediate nodes (_routers_) will help on retransmitting the message until it reaches its destination.
   The data is grouped in _datagrams_ or _packets_ and this layer also needs an addressing mechanism.
   Nodes will have a _logical address_ and the most common one is the IP address.
1. **Transport**: provides a logical connection between two programs of different nodes.
   Both nodes can maintain multiple logical connections.
   The data is grouped in _segments_ or _user datagrams_ depending of the protocol used and it also requires an addressing mechanism which usually is a _port_ number.
1. **Session**: provides a way to establish a session for a logical connection. The session provides the mechanism for a _reliable_ communication and synchronisation between the nodes.
1. **Presentation**: it mainly provides the _data conversion_ (also known _serialisation_) of complex data structures that need to be sent.
   It can also provide data encryption/decryption or compression/decompression.
1. **Application**: provides the highest-level communication between 2 programs and it is specific of the programs themselves (email, web browsers, remote commands, etc.)

### TCP/IP

The TCP/IP model is published a few years after the first implementations where already in used so it was an attempt to formalise its use and development.
It is a more specific model as it describes what protocols should be used at some levels although other layers are not fully defined.
The semantics of each layer are very similar to the OSI one.

The layers of the TCP/IP model, from top to bottom:

1. **Application**: any protocol used by the 2 programs involved in the communication.
1. **Transport**: defines 2 possible transport protocols:
   - _Transport Control Protocol_ (TCP)
   - _User Datagram Protocol_ (UDP)
1. **Inter-network**: defines the _Internet Protocol_ (IP) used for transmitting data between nodes across different networks.
1. **Host to net**: allow IP datagrams to be delivered (or rejected) to another host of the same network.

### Hybrid model

The OSI and TCP/IP models are very similar. In fact, as the OSI model is so general, it can be simplified so it is adjusted to the TCP/IP model's layers.
For terminology simplicity, in this course we are going to follow an hybrid model with 5 layers:

- Application
- Transport
- Network
- Data link
- Physical

## Encapsulation and decapsulation

## Addressing fundamentals
