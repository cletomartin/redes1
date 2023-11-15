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

If we want to deal with complex communication problems, we will have to divide each problem into simpler functions or tasks that will collaborate to each other in order to get overall communication done.
This is an intuitive idea of _protocol layering_:
divide the communication problem into different phases which solve _a particular issue/problem_ of the overall communication process and _delegate_ the rest to other phases (previous or following ones).

```{note}
The Philosopher's analogy is an illustrative example. See that each layer of the communication use a information useful at its own level.
For example, the translator has a field called `L` for the language and the sender uses the fax number.
```

Protocol layering organises the communication mechanism in layers that:
- Are sorted by _abstraction level_, from the end user to the transmission medium.
- Require functionality from upper layers and provide it to the lower ones.
- At both ends, each layer can be seen as they maintain a virtual conversation that makes sense at the layer's level.

## Reference models

### OSI

### TCP/IP

## Addressing fundamentals
