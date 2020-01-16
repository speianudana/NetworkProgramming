import socket
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 2400)
print('connecting to %s port %s' % server_address)
print('To quit type exit')
sock.connect(server_address)
run_client = True

while run_client:
    print("Query example: select first_name last_name email")
    message = input("write query: ")
    print('Please wait for execution, sending: "%s"' % message)
    sock.sendall(message.encode())
    if message == 'exit':
        print('Exiting...')
        run_client = False
        sock.send(b"exit")
        sock.close()
        break
    received_value = ''
    while True:
        data = sock.recv(1024)
        data_received = data.decode()
        if "#done" in data_received:
            received_value = received_value + data_received.replace('#done', '')
            break
        received_value = received_value + data_received
    json_loads = json.loads(received_value)
    for element in json_loads:
        print(element)
