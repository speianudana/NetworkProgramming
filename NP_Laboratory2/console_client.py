import sys

from cryptography.fernet import Fernet

from application_layer import get_symmetric_key, show_server_result
from transport_layer import send, get_client_socket

sys.setrecursionlimit(10000)

key = get_symmetric_key()
symmetric_encryption = Fernet(key)
client_socket = get_client_socket(key)

while True:
    # send data to sever
    print('Send a message to server')
    message = input('Write request: ')
    if message == "exit":
        break
    send(client_socket, None, message, symmetric_encryption)
    # receive data from sever
    data, server = client_socket.recvfrom(8192)
    show_server_result(data, symmetric_encryption)
