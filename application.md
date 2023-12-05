b(application)=
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
- _Caching content_: which improves the overall user experience and reduces the shared bandwidth (typically at WAN links).
  We will see this example in depth later.

## HTTPS

## SSH

## DNS

## P2P
