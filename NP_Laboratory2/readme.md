## Laboratory 2
### Tasks:

1. Implement a protocol atop UDP

- With a method to make it more reliable, using either (1) error checking + retransmission (this is simple) or (2) error correction (a bit harder but cooler)
- Make the connection secure, using either symmetric streaming or asymmetric encryption


2. Then, once your protocol is more reliable and secure, make an application-level protocol on top of it, like FTP, or HTTP:
- A set of methods/verbs and rules on how to interact with it
- Model the protocol as a state machine, for documentation

To prove that everything is working as intended, make a server and a client using this nice protocol of yours.

Some optional tasks:
- Multi-streaming, like in SCTP
- Packet ordering
- Congestion control
- For the server, use epoll to make it concurrent
Links for the congestion control:
- https://stackoverflow.com/questions/19829286/python-nonblocking-sockets-and-reliable-udp
- https://stackoverflow.com/questions/8683722/how-can-i-do-congestion-control-for-a-udp-protocol

### How to run:
If you have Linux congratulations, else run on Ubuntu:
```
python3 udp_server.py
```
Then in any terminal:
```
python console_client.py
```
