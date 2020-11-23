import json, os, re, socket
import itertools


class QuerySocket:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((socket.gethostbyname('ipc_server_dns_name'), 8080))
        self.delta = 500
   
    
    def set_delta_money_range(self, delta):
        m = {'req' : 'set_money', 'data': delta}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)

        return recDecoded['res']
    
    def next_money_range(self):
        m = {'req' : 'next_money'}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)
        
        return recDecoded['res']

    def get_next_page(self):
        m = {'req' : 'next_page'}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)

        return recDecoded['res']

    def get_query(self):
        m = {'req' : 'get_query'}
        data = json.dumps(m).encode('utf-8')
        self.delta = 500
        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)
            
        return recDecoded['res']