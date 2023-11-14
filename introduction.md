(intro)=
# Introduction

This lesson is an introduction to computer network concepts and the Internet.
You can find the slides [here](slides/introduction.odp).

## What's a computer network?

A computer network is a set of _interconnected_ computers that can _exchange_ information.
A computer network is usually represented like a graph where:

- The _nodes_ may represent a _host_ (like a PC or smartphone) or a _connecting device_ (like a router or a switch).
  Nodes are considered _terminal_ devices while the connecting devices are typically used to interconnect other nodes or other networks.
- The _links_ represent a connection between the nodes. These links may be wired or through wireless signals. We will see different types of connections during this course.


```{note}
A network can be as small as 2 computers connected through a wired connection and it can be as large as millions of nodes.
```

A network can be measured with the following _criteria_:

- _Performance_: the network performance can be measured with in a different ways:

  - _Transit time_: the time needed by a message to travel between 2 nodes.
  - _Response time_: the time elapsed between a request and the arrival of its response.

  ```{note}
  _Throughput_ (the amount of information during a period of time) and _delay_ (the excessed time for a particular event) are often contradictory.
  ```

- _Reliability_: typically measured by the frequency of _failures_ in the network and its _robustness_ during failures.

- _Security_: whether the network is capable of protecting _unauthorised access_, _data loss_ and _data manipulation_.

The information in a network flows between the nodes through the links.
These information flows can be:

- _Simplex_: the information can only flow in one direction, from one node to another.
  For example: keyboards, TV signal.

- _Half-duplex_: the information can flow in both directions although only one node can transmit at certain time.
  For example: walkie-talkies.

- _Full-duplex_: the information can flow in both directions and both nodes can transmit at the same time.
  For example: telephone.

## Network classification

There are different criteria on which one could classify a computer network.

### By type of connection

The link is the connection between two nodes of the network.
This link can be of two types:

- _Point-to-point_: the link is established between 2 nodes of the network and can only be used by them.
  They are typically wired although they can be wireless (e.g. the TV remote controller).

- _Multipoint_: the link is established between nodes and it is shared across all of them.
  Since this is a shared medium, it has some problems that need to be addressed that are not present in a point-to-point link:

  - Sharing the transmission medium and its bandwidth (_spatially_ or _timely_ shared).
  - Addressing: in order to send information, we will have to use some _addressing mechanism_ so each node will be identified with an address.
    This mechanism may support the following variations:
    1. _Unicast_: the address identifies a single node in thet network.
    1. _Multicast_: the address identifies a subset of nodes of the network.
    1. _Broadcast_: the address identifies all nodes of the network.

### By physical topology

There is also another way to classify a network using the concept of _physical topology_.
It describes they way the network is laid out physically, how the links are arranged and connect different set nodes to each other.
The topology can be seen as a _geometric representation_ of the links and the linking devices to one another.

- _Mesh_: there is a point-to-point link from every node of the network to the rest of nodes.
  This means that for a network of `n` nodes, there will be `n ( n - 1) / 2` full-duplex links.

  - Higher robustness: if a link or node fails, there are alternative paths so the network can still function.
  - Higher security: communication happens in dedicated channels.
  - Higher cost: requires lot of links

- _Star_: there is a point-to-point link between the nodes to a centralised hub.
  This hub will be used as a shared linking device and will interconnect all nodes.
  So for a network with `n` nodes, there will be exactly `n` full-duplex links, each of them going from a node to the hub.

  - Lower cost: less complexity in terms of links required.
  - Lower robustness: the hub is a _single point of failure_.
  - Higher security: communication still happens in dedicated channels.

- _Bus_: there is a multipoint connection between nodes, a shared transmission medium (e.g. a cable called _backbone_) to which the nodes are attached (tapped).
  - Lower cost: less complexity in terms of links.
  - Limitation of the amount of nodes that can be attached.
  - Requires some kind of control on how to use the shared media (addressing, access, etc.)
  - In case of failure, localising the error can be challenging.
  - Security concerns about unauthorised access.
  - The shared medium is a single point of failure.

- _Ring_: each node of the network has 2 point-to-point connection to other 2 nodes on either side of it, forming a ring between all of them.
  The information flows in one direction reaching its destination jumping from one node to the following one in turn.
  - Easy and cheap to implement.
  - Each node can be now a potential single point of failure but the failure would be very easy to identify.
  - The unidirectional flow makes them slow.

### By size

In terms of the network size, we can distinguish:

- _IPN_: InterPlanetary y Delay Tolerant Networks (DTN).
- Global (Internet).
- _WAN_: Wide Area Network – country or continents.
- _MAN_: Metropolitan Area Network – towns or neighbourhoods.
- _LAN_: Local Area Network – buildings or departments.
- _PAN_: Personal Area Network – computes or desktops.
- _SAN_: System Area Network  – embedded systems.
- _NoC_: Network On Chip – networks in a integrated circuit.

We are going to focus in LAN and WAN.

#### LAN

A Local Area Network usually consists on hosts connected to one another.
They can use a shared bus (multipoing is not really common nowdays) or having connecting device where each node has a point-to-point connection to it (e.g. a switch or router).
Logically, it represents a network of nodes that can send information between them and node addresses identify each of them uniquely within the network.
It is common that today's LANs can reach transmission rates of 10Gbps and typically use a _simple topology_.

LANs are not rarely used in isolation.
Instead, they are connected to other LANs using WAN connections.

#### WAN

A Wide Area Network brings together connecting devices like routers and their associated hosts.
The links of a WAN are typically point-to-point between network devices (not hosts) and it is used for connecting larger entities like organisations or countries.

There are 2 types of WANs:

- _Point-to-point WAN_: where 2 connecting devices are connected to bring 2 different networks together.
- _Switched WAN_: when we need to connect multiple point-to-point WANs together then we will need to use switches between the connecting devices.
  As we will see soon, this is the structure of the backbone of global communication today.

## Inter-networks

This mix of LANs and WANs is very common today. It creates the notion of _inter-network_ (or _internet_) where two or more networks are connected each other.
Each network can use different technology and, as long they use the same communication rules, information can flow from and to different networks with no issues.

As we introduced before, switched WANs are required when we need to connect multiple networks.
It is required to form a _switched network_ between networks in other to create an internet.
In a switched network, data must be forwarded between networks somehow.
It can be done using:

- _Circuit-switched_ networks: the switches activate (or deactivate) connections between ends.
  This connections are established once and are kept active during all the data transmission until it is closed.
  This connection is called _circuit_.

  An example of this type of switched WAN is the "old" telephone system.
  The idea is that telephone terminals are connected to the switch and switches are connected with high-capacity links between them.
  Unless all telephone circutis are used at the same time, the high-capacity link will be not used at full capacity.

- _Packet-switched_ networks: instead of opening connections between communication ends,
  the ideas is to break down the data into small _packets_ that are transmited individually.
  This means that the packets can now be stored and sent later and organise the transmission differently than in a continous communication scenario.

  Computer networks (and also telephone systems nowdays) work using this approach.
  A _router_ can receive packets from the hosts, queue/store them and send them to the other router individually.
  Even if the link between routers is at full capacity, the fact that packets can be stored and queued


- _Packet-switched_ networks:

```{note}
Note the we are talking about an internet (with lowercase i) and as abstract concept.
```

### The Internet
### A brief history
