import select
import sys
from threading import Thread

from http_protocol_layer import parse_http_request
from transport_layer import get_server_socket, is_new_client_connecting

sys.setrecursionlimit(10000)

server_socket = get_server_socket()
f = open("private_key.txt", "w")

epoll = select.epoll()
epoll.register(server_socket, select.EPOLLIN)

while True:
    epoll_events = epoll.poll(10000)
    for descriptor, event in epoll_events:
        # Read data from a client socket
        data, address = server_socket.recvfrom(8192)
        if not is_new_client_connecting(data, address):
            # start a thread to process request
            Thread(target=parse_http_request, args=(data, server_socket, address), daemon=True).start()
