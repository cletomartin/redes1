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

```{note}
Note the we are talking about an internet (with lowercase i) and as abstract concept.
```

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
  Even if the link between routers is at full capacity, the fact each packets can be stored and queued by the routers make the network still functional, although some _delays_ might be introduced.

### The Internet

The most notable internet is the Internet (with uppercase I) and it is composed of thousands of interconnected networks.
The structure can be described as following:

- _Customer networks_: these are the end users that pay for a broadband connection for a home or an office.
- _Provider networks_: a user pay to an Internet Service Provider (ISP) to connect their customer network to the provider network.
  These providers (usually known as _regional ISPs_) pay for connecting their provider networks to the backbone networks of the Internet.
- _Backbone networks_: these are managed by some ISP (usually known as _international ISPs_) and they are interconnected using _peering points_,
  making that a message can be routed through the entire structure from one network to another.

There are different ways in which you could _access the Internet_:

- Using _telephone lines_: although not really common these days for end users,
  the telephone infrastructure can be used for accessing the Internet using a _modem_ or a _DSL_ line.
- Using _dedicated lines_: like fibre channel or TV cable, which is the most common way for end user's.
  It provides high-speed access compared to the telephone lines.
- Using _wireless lines_: there are remote locations in which case it is difficult to have wire-based technology.
  For these cases wireless lines like satellite links can be used to access the internet.
- Using _direct connection to the Internet_: for big organisations it is possible get a high-speed connection with a regional ISPs and connect its internets to the Internet.


#### Standards and administration

The Internet is currently organised and managed by the following bodies:

- _Internet Society_ (ISOC): is the main Internet organisation that provides support for the Internet standards and procedures.
- _Internet Architecture Board_ (IAB): is the technical advisor of ISOC, focused on the technical and researching matters of the Internet community.
  It has two main components:
  - _Internet Engineering Task Force_ (IETF): is a forum of working group, managed by the _Internet Engineering Steering Group_ (IESG) responsible of detecting problems and provide solutions to them.
    It is divided by _areas_ like applications, protocols, architecture, etc. There are _working groups_ on each area for developing solutions to specific topics.
  - _Internet Research Task Force_ (IRTF): is a forum of working group, managed by the _Internet Research Steering Group (IRSG) focused on long-term research topics about new technologies, architectures, applications, etc.


The _Internet standards_ are a very thoroughly tested specification for a particular functionality of feature of the Internet.
These standards will be followed by the Internet community so users and services can interoperate.

Before of having an Internet standard fully approved, it must go through a review process:

1. An _Internet draft_ is created in the first place.
   This in a work-in-progress, non-official document with a 6-month lifetime.
1. If authorities recommend it, the Internet draft is published as a _Request For Comments_ (RFC) document.
   A number is assigned to them and the RFCs will be assigned with a _maturity level_:

   - _Proposed Standard_: at this level, the RFC has generated enough interest so some groups have started to test and implement it.
   - _Draft Standard_: if two or more independent and interoperable implementations have been done, the RFC will be elevated to this level.
     Typically the original RFC will be modified as problems are expected to be found.
   - _Internet Standard_: a draft standard reaches this level after a demonstration of successful implementation.
   - _Historic_: typically reserved for those RFC with historical interest like superseded features.
   - _Experimental_: RFCs that should not implemented on any Internet service in production.
   - _Informational_: RFCs usually created by vendors that contain general or tutorial information.


#### A brief history of the Internet

The Internet evolved from a private network to a global one in about 40 years.
These some of the milestones of the Internet's history:

- **Before 1960**: during these years, computer networks were limited to some terminals connected to a mainframe by leased lines.
  The project RAND (Research ANd Development) started on 1947 with the aim of promoting the scientific knowledge for helping US security homeland.
  Some of the research results of this project will have impact on the birth of the Internet years later.
- **1961**: Leonard Kleinrock proposes packet switching.
- **1962**: J.C.R. Licklider published "On-Line Man Computer Communication".
- **1962**: Licklider was hired by the Defense Advanced Research Projects Agency (DARPA) to "interconnect the Department of Defense (DoD) main computers at Cheyenne Mountain, Pentagon and SAC" (ARPAnet).
  Three network terminals were installed: Santa Monica, Berkeley and MIT.
- **1967**: Creation of ARPANET: a small network whose hosts would have an _Interface Message Processor_ (IMP) to communicate with other hosts.
  The IMPs would be able to send and receive messages from other IMPs.
  Leonard Kleinrock proposes packet switching.
- **1968**: Douglas Engelbart and the Augmentation Research Center (ARC) present the oN-Line Ssystem (NLS),
  a computer collaboration system where multiple users could interact.
  That event was known later as "The mother of all demos".
  The NLS was the first system including graphic interface, desktop, icons, mouse, windows, hyperlinks and video-conference.
- **1969**: RFC 1 "Host software", specifying what is in the IMPs and what in hosts.
- **1969**: First ARPANET: 4 nodes in University of California at Los Angeles, University of California at Santa Barbara, Stanford Research Institute, and University of Utah.
- **1971**: ARPANET grows to 15 nodes. It worked with the Network Control Protocol (NCP).
- **1971**: Ray Tomlinson sends the first email.
- **1971**: File Transfer Protocol (FTP) is defined.
- **1973**: Robert E. Kahn and Vinton Cerf work in a common internetwork protocol, as an improvement of NCP.
- **1974**: RFC 675 "Specification of Internet Transmission Control Program", by Vinton Cerf.
- **1977**: An internet of 3 different networks (ARPANET, packet radio, and packet satellite) was demonstrated.
- **1981**: ARPANET has 213 nodes.
- **1981**: RFCs 791-793 define the basics of TCP/IP.
- **1983**: 1 January was "the flag day": TCP/IP replaced all earlier protocols in ARPANET.
- **1983**: Paul Mockapetris proposes the protocol Domain Name System (DNS).
- **1983**: Berkeley Unix 4.2BSD includes the socket API.
- **1984**: 4 Berkeley students write Berkeley Internet Name Domain (BIND), the DNS Unix first implementation.
- **1985**: IETF is created.
- **1989**: First ISP "TheWorld.com" in the US.
- **1991**: Tim Berners-Lee (at CERN) develop the first network based hypertext implementation and the HTTP protocol in the "WorldWideWeb" project.
- **1993**: University of Illinois creates the Mosaic graphical web browser.
- **1994**: Classless Inter-Domain Routing.
- **1998**: IPv6.
- **2008**: 1500 M-users.
- **2023**: 5200 M-users (90% in developed countries and 57% in developing countries)

#### Economy around the Internet

Nowdays the biggest and most-valued companies in the world has grown based on the existence of the Internet.
These are a few examples of this type of companies:

- _Amazon_: founded in 1994, initially based on the e-commerce bussiness, runs Amazon Web Services (AWS)
  which is used by companies and developers for running lots of Internet services.
  - Revenue (2022): $513.98 billion
  - Employees (2022): 1,112,555
- _Alphabet_: founded in 2015 for re-structuring Google, the famous web search engine.
  - Revenue (2022): $282.8 billion
  - Employees (2022): 181,798
- _Meta_: founded in 2004 and originally as the social media Facebook, is an Internet-based company focused on communication and marketing research.
  It is also the owner of Instagram and WhatsApp, among others.
  - Revenue (2022): $116.61 billion
  - Employees (2023): 66,185
- _Microsoft_: founded in 1975 and they are currently focusing on its cloud service called Azure.
  - Revenue (2023): $211.9 billion
  - Employees (2023): 238,000
- _ByteDance_: founded in 2012, they are the owners of TikTok.
  - Revenue (2022): $85.2 billion
  - Employees (2023): 150,000
