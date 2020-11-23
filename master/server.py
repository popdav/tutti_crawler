import socket, sys
from client_thread import ClientThread
from query_queue import QueryQueue

class Server():
    def __init__(self, port):
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queryqueue = QueryQueue()
        self.run_server = True

    def kill_server(self):
        self.run_server = False
        
        try:
            self.serversocket.shutdown(socket.SHUT_RDWR)
            self.serversocket.close()
        except:
            pass
        
        

    def start(self):
        self.serversocket.bind((socket.gethostbyname('ipc_server_dns_name'), self.port))
        # print(socket.gethostname())
        self.serversocket.listen(10)

        print(f'Server working on port: {self.port}')

        while self.run_server:
            try:
                (clientsocket, address) = self.serversocket.accept()
            except:
                break
            print(f'Client accepted: {address}')
            ct = ClientThread(self.queryqueue, address, clientsocket)
            ct.start()

if __name__ == "__main__":
    server = Server(8080)
    server.start()