import socket
from threading import Thread

from Utils import parse_result, request_server_result


class ClientThread(Thread):

    def __init__(self, ip, port, connection, server_result):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.connection = connection
        self.server_result = server_result
        print("Client connected " + ip + ":" + str(port))

    def run(self):
        # in an infinite loop waiting for client commands
        while True:
            data = self.connection.recv(2048).decode()
            print("Server received data:", data)
            if data == 'exit':
                self.connection.close()
                break
            result = parse_result(self.server_result, data)
            print("Sending to client result: ", result)
            self.connection.sendall(result.encode())
            self.connection.send(b"#done")


server_address = ('127.0.0.1', 2400)
print('Getting data from server')
server_result = request_server_result()
print('Done, listening to client connections')
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listen to the connections from the localhost and the given port
tcpServer.bind(server_address)

while True:
    # listen to max 4 simultaneously connections
    tcpServer.listen(4)
    print("TCP Server: Waiting for connections...")
    (connection, (ip, port)) = tcpServer.accept()
    # start a thread to listen the client select commands
    ClientThread(ip, port, connection, server_result).start()
