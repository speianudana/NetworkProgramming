import json

import error_correction
from transport_layer import get_secret_key, send

data_base = dict()


def parse_http_request(data, server_socket, address):
    data = error_correction.decode(data.decode())
    fernet_encryption = get_secret_key(address)

    if fernet_encryption is not None:
        client_data_decrypted = fernet_encryption.decrypt(data.encode())
        message_from_client = client_data_decrypted.decode()
        print('Received data: {}'.format(message_from_client))

        if message_from_client == "get /data":
            get_data_request(server_socket, address, fernet_encryption)

        elif "delete /data" in message_from_client:
            delete_data_request(message_from_client, server_socket, address, fernet_encryption)

        elif "put /data" in message_from_client:
            put_data_request(message_from_client, server_socket, address, fernet_encryption)
        else:
            send(server_socket, address, "Wrong command. Think a bit :D", fernet_encryption)


def get_data_request(server_socket, address, fernet_encryption):
    header = "GET / HTTP/1.1 200 OK\r\nHost: /get\r\nContent-Type: text/json\r\n\r\n"
    add_http_header_and_send(data_base, header, server_socket, address, fernet_encryption)


def delete_data_request(message_from_client, server_socket, address, fernet_encryption):
    header = "DELETE / HTTP/1.1 200 OK\r\nHost: /delete\r\nContent-Type: text/json\r\n\r\n"
    if "?" in message_from_client:
        try:
            params = message_from_client.split("?")
            print(params)
            params_keys = params[1].split(",")
            print(params_keys)
            for param in params_keys:
                del data_base[param]
        except IndexError:
            send(server_socket, address, "Wrong parameters received", fernet_encryption)

    else:
        data_base.clear()
    add_http_header_and_send(data_base, header, server_socket, address, fernet_encryption)


def put_data_request(message_from_client, server_socket, address, fernet_encryption):
    if "?" and "=" in message_from_client:
        try:
            params = message_from_client.split("?")
            params_keys = params[1].split(",")
            for param in params_keys:
                param_values = param.split("=")
                data_base[param_values[0]] = param_values[1]
        except IndexError:
            send(server_socket, address, "Wrong parameters received", fernet_encryption)
    header = "PUT / HTTP/1.1 200 OK\r\nHost: /put\r\nContent-Type: text/json\r\n\r\n"
    add_http_header_and_send(data_base, header, server_socket, address, fernet_encryption)


def add_http_header_and_send(data_base, header, server_socket, address, fernet_encryption):
    json_dumps = json.dumps(data_base)
    json_response = header + json_dumps
    send(server_socket, address, json_response, fernet_encryption)
    return json_response
