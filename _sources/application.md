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

The application layer requires service from the transport layer.
The kind of service and the performance needed is determined by the own nature of the application.
The following metrics are usually relevant for most of applications:

- _Data loss_: the amount of data that can be lost at different points of the communication path.
  Some applications tolerate some degree of data loss (e.g. video transmission) whereas others require 100% reliable data transfer (e.g. file transfer).
- _Bandwidth_: the amount of data transferred per time unit.
  Some applications requires a minimum of bandwidth to be "usable" (e.g. videoconferencing) whereas others can adapt themselves to changes in available bandwidth (e.g. modern video players).
- _Timing_ or _delay_: the amount of time between a request and its response.
  Some applications requires a very limited delay to be "usable" (e.g. games) whereas others might tolerate higher delays (e.g. messaging).

```{note}
Show the table with different types of applications and their requirements of the transport layer
```

The Internet protocol stack provides 2 protocols: TCP and UDP.
These protocols provide the following services:

- _TCP service_: provided by the TCP protocol and has the following features:
  1. _Connection-oriented_: a virtual connection is established between client and server.
     This connection is created before client and server start to exchange transport messages.
  1. _Reliable_: there is some level of guarantee that messages will arrive to destination.
  1. _Flow control_: so the sender cannot overwhelm the receiver.
  1. _Congestion control_: so the data flow is adapted by if the network is overloaded.

  Note that TCP does not resolve some communication issues like _timing_ or _guaranteed bandwidth_.

- _UDP service_: it does _not_ provide any of the TCP service features, so it is not reliable.

We will study them in depth in the [transport](transport) chapter.

```{note}
Show the table with different protocols and the transport layer associated to them.
```

## Implementation example

One common way to implement applications that require communication is using the _socket interface_.
Sockets are an abstraction provided by the operating system for sending and receiving data using by using the transport layer.
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

The World Wide Web (WWW or Web) is a distributed service that provides access to documents called web pages.
The web page content has evolved from plain text to multimedia content like videos, audios, etc.
These two features have made the web to be highly scalable:

- Highly _distributed_: they can be placed in different physical locations.
  The place where web pages are located is called _web sites_.
- The are _linked_: they can refer to each other, even though they are not placed is the same server.
  The concept from 1963 of _hypertext_, where a document can refer to another and the reader can access to it directly, has evolved to _hypermedia_ because the linked objects are not only text anymore (video, audio, etc.)

It was originally created by Tim Berners-Lee in 1989 at CERN for allowing researchers to access scientific content from other researchers.

### Web browser

In order to get access to web pages and their content a special application is needed: a _web browser_ or _web client_.
This program is able to request and receive content that is shown to the user.
It also handles the user input and transform it into requests.

```{note}
Show the 3 components of the web browser.
They work as follows:

1. The _controller_ handles the user input and transform it into specific actions of the client programs.
1. Each client program knows how to access a specific _protocol_, so if the user requested a document via HTTP, the HTTP client will be used to get it.
1. Once the document is retrieved, the controller uses the _interpreters_ to render that document on the screen.
```

Web browsers handle 3 types of web pages:

- _Static_ pages: these documents that are stored in the server and the client gets a copy as they are.
  Typical static files are HTML, XML, XSL, XHTML, etc.

  ```{note}
  Good things:
  - They are simple and fast.
  - Low workload for the server.

  Bad things:
  - No dynamic content which limits application scopes.
  - Hard to maintain as the web site grows.
  ```

- _Dynamic_ pages: when they are requested by the client, the server _generates_ the content that is returned to the user.
  Each request might generate different content.

  ```{note}
  Good things:
  - Content can be programmatically generated.

  Bad things:
  - High workload for the server.
  - Slower than static files.
  ```

- _Active_ pages: when they are requested by the client, the server responds with a program that will be executed by the web browser.
  This program will finally generate the web page that will be show to the user.

  ```{note}
  - Good things:
    1. Content can be programmatically generated.
    1. Low workload for the server.


  - Bad things:
    1. Web browsers need to run programs (become interpreters).
    1. Security and privacy concerns.
  ```


Web pages can be referenced in the web browser using a Uniform Resource Locator (URL).
A URL is a general mechanism for referencing objects in a structured way.
This is its format:

```text
<method>://<host>[:<port>][/<path>]
```

Where:

- `method` is the protocol to use. For example, `http` or `ftp`.
- `host` is the IP or the host name of the server. For example, `google.com` or `www.hola.es`.
- `port` is the destination port of the transport communication. By default is `80` for `http`.
- `path` is the place of the target object. If not specified, it will take the root document (typically `index.html` in `http`).

For example:

```text
http://www.someschool.edu/someDept/pic.gif
ftp://my-server:631/contacts.csv
```

### The HTTP protocol

The HyperText Transfer Protocol (HTTP) is a protocol that origianlly was created for retrieving web pages.
It defines how to a client and a server have to be implemented in order to provide all the required operations.
This protocol uses:

- TCP as transport protocol.
- The HTTP server will be listen at port 80.

The clients sends _HTTP requests_ to the server and this returns _HTTP responses_.
For example, a web browser exhanges HTTP messages with a web server to retrieve web pages.

The protocol HTTP is _stateless_ meaning the server will not maintain information about past requests from clients.
HTTP can be configured to use TCP in two different modes:

1. **Nonpersistent HTTP**: for each web page object, there will be a new TCP connection.
   This means that each HTTP request-response will generate a new TCP connection each time.

   ```{note}
   The example is a file HTML that includes an image.
   There are 2 different TCP connections due to it is not persistent.
   Note that each TCP connection needs the 3-way handshake to be established, which is expensive if there are lot of objects.
   ```

1. **Persistent HTTP**: multiple web page objects can be sent over the same TCP connection.
   This reduces the amount of overhead required for each connection but might increases the amount of connections that a single server holds for a period of time.

   ```{note}
   The example now is much simpler than the nonpersistent one
   ```

The HTTP procotol defines 2 types of messages:

- **Requests**: messages sent from clients to the servers.
  They have 4 fields:
  1. _Request line_:
     - Method: we will see them in depth a bit later.
     - URL: the targeted object of the request.
     - Version: the HTTP protocol version to use.
  1. _Header lines_: headers are used to provide options and more context to the request.
     It can be empty.
  1. _Blank line_: just a line break made of 2 characters `CR` and `LF`.
  1. _Body_: if the requests require to have data to be sent to the server,
     the body may be the place for them.

  ```{note}
  Show the example of the HTTP request parts.
  The `Connection` header indicates that this is a nonpersistent request.
  ```

  The main request methods are:

  1. `GET`: retrieve a specific object or resource. Its body is body is empty but it can pass some information to the server using:
     - The headers.
     - The URL parameters e.g. `http://uclm.es/info?edificio=1&campus=CR`
  1. `HEAD`: similar to `GET` but only retrieve metadata about the resource,
     like the last time the resource was modified.
  1. `PUT`: sends a document to the server which is the reverse of `GET`.
  1. `POST`: sends some information that the server should add or manipulate, like form data.

  ```{note}
  Show the table of HTTP request headers.
  Mention that `Cookie` will be seen in depth.

  Also comment that the request headers shown in the slides are just of a subset of the standard ones.
  There can be custom headers defined by the application themselves.
  ```

  Apart from the request headers we have seen, The headers might also be

- **Responses**: messages sent by the servers to the clients.

  They have 4 fields:
  1. _Response line_:
     - Version: the HTTP protocol version to use.
     - Status code: an integer representing the response type.
       We will see them in depth a bit later.
     - Phrase: a string version of the status code.
  1. _Header lines_: headers are used to provide more context to the client in the response.
     It can be empty.
  1. _Blank line_: just a line break made of 2 characters `CR` and `LF`.
  1. _Body_: if the reponse includes data the body may be the place for them.

  The status codes are 3-digit integers whose meaning is divided in groups:

  - `2XX`: successful group. `200` means the request was successful.
  - `3XX`: redirection group. `301` means the requested object was moved to another location, specified by the `Location` reponse header.
  - `4XX`: client-side error group: `400` means the request was not valid and `404` means the requested object was not found.
  - `5XX`: server-side error group: `500` means a general server error happened and `505` means the server does not support the specified HTTTP version.

```{note}

Comment that response headers shown in the slides are just of a subset of the standard ones.
There can be custom headers defined by the application themselves.

About the following examples of the slides:

1. The HTTP GET example shows a GET request for the object `/usr/bin/image1` using HTTP version 1.1.
   The tells to the server that it accepts both `gif` and `jpeg` images.
   The server's reponse contains the image with a few more metadata: the server that relied, the image size, the format in which the image is encoded, etc.

1. `httpbin.org` is a dummy HTTP server that provides information about the requests it receives. It can be useful for testing HTTP request development.
   In this example we are using it to create a request using _netcat_. `nc` will create a TCP connection to port 80 and send the data we type on the console.
   When a blank line is introduced, the GET request will be made.

   Note that the connection is kept open. If you use `Connection: close` as header, after the request the connection will be closed.

1. `curl` is a command-line tool for interacting with HTTP servers. It helps to create debug and create scripts that need to access resources via HTTP (download a file, request for a service, etc.).
   In this example `curl` recevies a `301` meaning that `google.es` is actually `www.google.es`, `curl` creates another request to the new URL automatically.

   You can show this step by step if you firstly don't use `-L` flag. That will make `curl` not following the new location automatically.

1. In the HTTP PUT example the client requests the execution of a CGI `/cgi-bin/doc.pl` (a Perl script).
   In this case, the request does contain input data (50 bytes) for the script.

   The server runs the script with the input data and generates a response with a dynamic object that goes in the response body (2000 bytes).

1. Again, `nc` can be used for creating a PUT request. Note that if `Content-Length` is not provided, the server will response as soon as the first blank line is sent.
```

### Cookies

As we previously said, the HTTP protocol is stateless.
This means that the communication parts need to track any context or state related to the communication.
For example, the server does not recall that a certain client already made a related request before.

The use of HTTP in many different types of applications has forced the introduction to keep some context or state.
For example, a shopping cart or authenticated users of a given web page are examples that having some kind of context will improve notabily the user experience.

A way to implement this stateful mechanism is using _cookies_.
A cookie is usually a string value that encondes information about the user and their context.
For example it can include the domain name, user name, timestamps, etc.
It is _created by the server_ and passed to the client for them to store it (in their file system) during the client's first request.
The idea the client will send the cookie along their requests os the server can identify them and get the previous context.

```{note}
Explain the toy store example: the shopping cart is implemented using a cookie.
Note that the headers used are `Set-Cookie` and `Cookie`.

You can also show a cookie analyser like [this](https://termly.io/products/cookie-scanner/). Search for `http://uclm.es` there and you will see the cookies stored by the user.
```

### Proxies and web caches

We have seen a direct communication bewteen clients and servers so far.
However, it is possible to have intermmediate HTTP nodes that will act on behalf of the clients to contact the servers.
These nodes are called _proxies_ and they are useful in multiple scenarios:

- _Security and audit_: some work environments require to be secure and confidential.
  The use of proxies is useful for auditing the activity of web browsing as well for applying policies for access restrictions (forbidden web sites, user access control, etc.).

  ```{note}
  Show the `curl` example with `api.ipify.org`. The returned IP is the public IP from where we requested the HTTP GET.
  When we use a proxy with `http_proxy` envarionment variable, the returned IP will be the proxy one instead of the previous one.
  If the example proxy IP does not work you can get different one from [this list](https://www.proxyscrape.com/free-proxy-list).
  ```

- _Caching content_: which improves the overall user experience and reduces the shared bandwidth (typically at WAN links).

  ```{note}
  Show the diagram where 2 clients use a proxy as a web cache.
  The first one requests an object that is _not_ cached, so the proxy has to retrieve it from source.
  The second one requests an object that is cached so the response is much faster by saving an external call.
  ```
  The main reasons for using a web cache are:

  1. Improve client's experience as the response time is reduce overall.
  1. Reduce the use of the _access link_, i.e. the WAN connection that is typically shared across the organisation to access the Internet.
  1. Helps to those content providers with lower resources to effectively deliver content.

  ```{note}
  Explain the numeric example of how a web cache improves the user experience without increasing the cost too much:

  1. The response time for this case is `4.01` seconds.
  1. Increasing the bandwidth of the access link will reduce the response time to `3.1` seconds.
     This is usually an expensive upgrade.
  1. Using a web cache with a 40% chance of hits and no access link upgrade, the average response time will be `3.6`.
  ```

## TLS and HTTPS

Nowadays, HTTP is used in very different environments.
With more application being capable of providing services on the Internet,
the need of having _secure communication_ between clients and servers have been important in the recent years.

Think about the following applications:

- A bank's web application where users can make payments.
- Transport-related applications like a place for buying flight tickets.
- Email web portals where people can receive and send emails from their accounts.

These applications need to be protected from authorised use and HTTP nor TCP provide any help for this.
This is where protocols like Transport Layer Secure (TLS) or Secure Sockets Layer (SSL) are designed for.
The first one is the most recent version of the latter.
It can be used by any application protocol but when it is used in conjunction with HTTP it is known as HTTPS.
If a server supports HTTP with TLS, the URL changes from `http://` to `https://` and the protocol changes from `80` to `443`.

TLS provides the following services:

- _Fragmentation_: application messages are divided in fragments of $2^{14}$ bytes.
- _Compression_ (optional): fragments are compressed with the algorithm negotiated by client and server.
- _Integrity_: ensures that data is not modified on-transit.
- _Confidentiality_: data is encrypted so unauthorised access is not possible.
- _Framing_: a header is added to the encrypted payload creating a _frame_ which is passed to the transport layer.

These are important given the shared nature of the Internet: there are many places where information can be accessed by unauthorised actors.

TLS defines 4 protocols to achieve all these services:

1. _Handshake protocol_: client and servers need to agree on TLS communication details like what algorithms to use, what type of encryption, etc.
   Both also need to authenticate each other.
   They have to make sure that the other part is actually a legit one.
1. _ChangeCipherSpec protocol_: this protocol is used for signalling to client and server that when it is time to use for real the parameters and secrets exchanged during the handshake.
1. _Alert protocol_: when an error is detected, client and server will use this protocol.
1. _Record protocol_: all messages from the previous protocols will be processed by this layer that will transform the TLS messages into encrypted and signed frames.

```{note}
The example is just a TLS handshake to `google.es`.
The real output is longer because it includes the certificates from the server.
We do not need to explain them in detail, just mention that it is a way to authenticate that the server we are hitting is actually a Google's one.

The result of the TLS handshake is correct and some of the encryption parameters are shown.
```

## DNS

One important part of an URL is the _host name_ or _host address_.
This can be the IP of the server but human users are not good at remembering sequences of 4 bytes.
The Domain Name Service (DNS) is what helps in this situation: it provides a mapping between a host name made of characters to the corresponding IP addresses.
In this context, we will say that _a host name is resolved to its IP_ when a host name is translated to its corresponding IP address.
For example `google.es -> 142.250.200.131`.

DNS can be seen as a _distributed and hierarchical database_ which is accessible via _name servers_.
These name servers communicate with clients and routers using the _DNS protocol_ for resolving names.
The service is distributed because it cannot be centralised for the following reasons:
- Avoid single points of faiure.
- If used globally, the amount of traffic will be huge to be handled by a centralised service.
- Distance between clients and the central server will be different depending on the client's location.

Apart from name resolving, DNS provides the following services too:
- _Host aliases_: a server can be accessed by an _alias_ of a _canonical_ name.
- _Mail_: it contains information about mail servers and its aliases.
- _Load balancing_: there can be multiple IPs assigned to the same name.

### Hierarchical structure

DNS uses a _hierarchical_ name space.
This means that DNS names are structured in a specific way so each part of the structure corresponds to a certain level of the DNS server structure.

The structure of DNS names can be seen like a _tree_:
- Each node in the tree has a _label_ no longer than 63 characters.
- The root node has an empty label.
- A node can be referenced by its _domain name_, the path of labels separated by dots.
  If the domain name goes from the target node to the root node is known as _fully qualified domain name_ (FQDN).

```{note}
In the example of `pc1.dept.uni.edu.`, we can show that:

- That's a FQDN.
- We have 5 labels: `pc1`, `dept`, `uni`, `edu` and the empty label of the root node.
- We have 4 domain names: `pc1.`, `dept.`, `uni.` and `edu.`.

It is good to say that a _domain_ is any subtree of the name space.
For example: `dept.uni.edu.` is a domain.
```

The DNS servers are structured in a very similar way so they can be scalable to a large distributed system.
Each node of the tree might have a corresponding server that provides the information of all the nodes under that domain name.
This is known as _zone_ and the servers responsible of a zone create a _zone file_ with a list of all nodes under that domain.

```{note}
In the example, the `com` zone is huge so if the com DNS servers need to create the list of all nodes under this domain would not be scalable.
For that reason, subdomains like `yahoo.com` or `amazom.com` will hold the zone file for their own domains.
That way the `com` server can refer to any of the subdomains if more detailed information is needed.
```

### DNS servers

- _Root servers_: there are 13 root name servers worldwide, each of them named after a letter (from A to M).
  They do not really store too much information as the details are delegated to other subdomain servers.
- _Top-Level Domain servers_: these are placed at the following level of the root servers and they are responsible of domains like `com`, `edu`, etc.
  and also top-level country domains like `es`, `uk`, etc.
  They usually do not hold detailed information about other domains of their zone.
- _Authoritative DNS servers_: these servers are contacted by TLD ones as they are delegated to managed a subdomain and know all the hosts within their zone.
  For example, `google.com.` has `ns1.google.com` as one of the authoritative servers for their domain.
- _Local name server_: it is the name server that DNS clients will contact directly when they need to create a DNS query for resolving names.
  It can be maintained by an ISP or an organisation.


### DNS resolution mechanism

When a DNS client creates a query for a specific DNS name, it will firstly contact to its local name server and, if it does _not_ know the answer, it will trigger the query to the rest of the DNS network.
At that point, two strategies are possible: _recursive_ or _iterative_.

```{note}
The example shows two ways on how the name resolution of `gaia.cs.umass.edu` can take place:

1. _Recursive_: the local DNS server contacts a root server. The root server does not know about `gaia.cs.umass.edu` and asks for more information to `.edu` TLD server.
   The TLD server does not know about `gaia.cs.umass.edu` but it knows that for `cs.umass.edu` can contact to `dns.cs.umass.edu` authoritative server so it asks for it.
   This final authoritative server knows the answer for `gaia.cs.umass.edu` so the response goes back through all the previous path.

1. _Iterative_: the order of the DNS queries are the same but it is performed by the local name server instead by each DNS server in turn.
   For that to be possible, those servers that do not know the answer for `gaia.cs.umass.edu` will have to provide a server to ask instead.
```

Recursive queries clearly _simplifies the implementation_ of the local server but puts a _burden_ on the root and TLD servers.
Iterative queries makes the local name server to work more on each query and remove the pressure from the root and TLD servers.
This approach is more interesting for a global service like DNS.

In both cases, for DNS to scale and function properly in a global context, it is important that responses can be _cached_.
Caching responses for a period of time known as time-to-live (TTL) will reduce the amount of queries in the DNS network.
For example, the TLD servers are usually cached by the local name servers so the root name servers are not queried very often.

### DNS records

As we said before, DNS is a distributed database.
This database defines different types of _records_ that will hold information about the nodes.
They are stored as _resource records_ (RR) with the following format:

```
(domain name, type, class, ttl, value)
```

Where:
- _Domain name_: identifies the resource record.
- _Type_: the way the value needs to be interpreted (we will see more later).
- _Class_: can be different values but we are only interested in `IN` (means Internet).
- _Value_: the value of the record.

These are some types:

- `A` record: defines the IP for a given hostname,
- `NS` record: defines the authoritative name server for a given domain.
- `CNAME` record: defines an alias for a canonical name.
- `MX` record: defines the mail server for a given name.
- `SOA` record: provides information of a zone and domain.

### DNS messages

The messages can be _queries_ or _replies_.
Both use exactly the same message format:
- _Header_: 6 fields of 2 bytes each (12 bytes):
  - `identification`: an 2-byte integer that will be generated during the query and will be used in the replies to identify the original query.
  - `flags`: a set of bits representing different conditions of the message. For example:
     - _Is this a query or reply?_
     - _Is this reply authoritative?_
     - Error status.
  - The rest of the fields depend on if we send a query or receive a reply and point to the next variable section.
- _Content_: these fields might include the questions for queries and the responses for the replies.

### Examples

```{note}
The following examples will be used for a better understanding:


1. Adding a new DNS record like `redes1-esi.es` requires that an entity that is authorised for it (a _registrar_)
   updates the TLD servers with new information.
   In this example we use a domain provider like IONOS to:
   - Register our domain `redes1-esi.es`.
   - Point `www.redes1-esi.es` to our web server at `10.20.30.40`.

   Once it is done, people could access our new web site by doing the normal resolve mechanism:
   - `www.redes1-esi.es` will contact to the `.es` TLD server.
   - The TLD server will say it does not know about it but we should contact `ns1029.ui-dns.de` for getting more information.
   - The DNS client will contact this new name server and it will return the answer thanks to the A record it holds.

1. Show `/etc/resvol.conf` and `host` command.
1. Show `dig` command. The `PTR` record provides the domain name associated to an IP.
```

## SSH

The Secure SHell (SSH) protocol is was originally created for replacing the insecure protocol TELNET.
The main use of this protocol is to open terminal sessions on remote servers (commands `ssh` or `PuTTy`).
This is very useful, for example, for maintaining infrastructure remotely without the need of being physcailly present.
However, this protocol is general enough so it can be used for other purposes:

- File transfer: `sftp` and `scp` are applications that can transfer files securely over an insecure transport.
- Port forwarding: this is a generalisation of sending and receiving data over a secure channel.
  If we want to communicate 2 applications and provide a secure transport between them we can:
  1. Create an SSH tunnel between both nodes.
  1. Configure the end of each tunnel so the data received on through it will be redirected to the application ports.

  This way, it is possible to encrypt any type of traffic (HTTP, DNS, etc.).

The SSH stack defines 3 protocols:

1. _SSH-TRANS_: this layer is closed to the transport layer and is in charge of creating a secured transport layer.
   It will provide:
   - _Confidentiality_ and _integrity_ of the data transmitted.
   - _Compression_ which improves the performance of the communication.
   - _Server authentication_ that allows the client to ensure the server is actually who claims it is.

1. _SSH-AUTH_: once the secure transport is in place, SSH-AUTH allows client and server authenticate each other.
   Client initiates its authentication and based on the protocol negotiated it may or may not get access to the server.
   The mechanism is very similar to TLS.

1. _SSH-CONN_: once the client and server are authenticated and ready for starting to exchange data,
   this layer helps the client to create communication _channels_.
   Each channel can be used for one purpose (remote command execution, file transfer, etc.).
   This layer multiplexes data between the available channels.

```{note}
The SSH example requires to run a local SSH server.
It can be done using the following command:

:::
docker run --rm -e PASSWORD_ACCESS=true -e USER_PASSWORD=redes1 -e USER_NAME=redes1 -ti linuxserver/openssh-server
:::

It would be good to explain briefly:

- The first run just request the user name and password.
- The second run show the verbose output where some part of the negotations between client and server is shown.
- If we stop the SSH server and restart it again,
  the host key has changed so SSH will warn us that the server is not the same as we firstly contacted.
```

## P2P file sharing

Peer-to-peer is a different paradigm of application communication.
Instead of having a clearly separated role like client-server,
each node of the network can act as a client or a server _at any time_.
This is the reason because the nodes are known as _peers_.

P2P is used in multiple applications these days:
- File sharing.
- Voice communication.
- Blockchain.

File sharing services are commonly implemented using a P2P.

```{note}
Show the P2P example about Alice and Bod file sharing.
The key points to show are:
1. All nodes can be servers so this type of communication can be _highly scalable_ and provide _high availiability_.
1. The problem with this approach is the quality of the content distributed by the peers. It might be the case that some files are not fully available as there are parts none of the peers provide.
```

When peers ask for an object to the network, they need to know something how to locate other peers.
A possible solution is to use a _centralised directory_ (as Napster was implemented originally).
The idea is each peer will inform to a central server about how to be contacted and the content they can server.
The problem with this approach is that the central directory is now a _single point of failure_.

Another approach is to have multiple ways to maintain this peer directory.
This is the case of BitTorrent, where people can distribute metadata files (`.torrent`) that hold information about peers and their content.
On top of this, there are also multiple _tracker servers_ that keep track of the peers as well.
This approach avoids the single point of failure and provide high availability to the peer directory.

BitTorrent also improves the P2P file sharing service by making the following assumptions:

1. All files are broken in blocks of 256KB.
   Shorter sharing blocks allow peers to enter and leave the network more often without causing too much interruption to others.

1. Those blocks that are not common are requested first in order to increase their availability.
   That way, clients will balance the availability of the content evenly.

1. The distribution of the metadata files is not managed by the P2P network itself.
   It needs to be done with some other mechanism.

   The metadata file usually contains:
   - The name of the file.
   - The total size of the file.
   - The URL to a tracker.
   - The length of each piece (usually 256KB).
   - A list of hashes: one hash per piece.

In order to encourage clients to share files, BitTorrent defines a client relationship policy _tit-for-tat_: at first, the client is collaborative but later it will replicate to others what others do to it.
If the client shares lot of files, it will become a _seeder_ which will have better reputation across the network.
However if the client do not share much and only downloads from others, it will become a _leech_ which will decrease its reputation.


## Exercises

> TBD
