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

- _Point-to-point_:

- _Multipoint_:

### By topology

- _Mesh_
- _Star_
- _Bus_
- _Ring_

### By size

- LAN
- WAN

## Inter-networks

### The Internet
### A brief history
