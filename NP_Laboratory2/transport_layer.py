import socket

from cryptography.fernet import Fernet

import error_correction

IP = "127.0.0.1"
CLIENT_HEADER = "client:"
PORT = 1234


# send data to server/client
def send(udp_socket, client_address, server_message, encryption):
    server_message = encryption.encrypt(server_message.encode('utf-8'))
    humming_encoded_message = error_correction.encode(server_message.decode('utf-8'))
    if client_address is not None:
        # Send to client
        udp_socket.sendto(humming_encoded_message.encode(), client_address)
    else:
        # Send to server
        udp_socket.send(humming_encoded_message.encode())


def get_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    # Now setting server to non-blocking mode
    server_socket.setblocking(False)
    print(f'Listening for connections on {IP}:{PORT}...')
    return server_socket


def get_client_socket(key):
    server_address = (IP, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect(server_address)
    client_key = CLIENT_HEADER + key.decode()
    client_socket.send(client_key.encode())
    print(f'Connected to server: {IP}:{PORT}...')
    return client_socket


def is_new_client_connecting(data, address):
    if CLIENT_HEADER in data.decode():
        file = open("private_key.txt", "a")
        ip, port = address
        file.write(str(ip) + ":" + str(port) + "|" + data.decode().split(CLIENT_HEADER)[1] + "\n")
        file.close()
        return True
    else:
        return False


def get_secret_key(address):
    file = open("private_key.txt", "r")
    for line in file:
        ip, port = address
        if str(ip) in line and str(port) in line:
            symmetric_encryption = Fernet(line.split("|")[1].replace("\n", "").encode())
            return symmetric_encryption
    return None
