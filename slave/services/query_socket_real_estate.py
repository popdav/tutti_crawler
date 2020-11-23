import json, os, re, socket
import itertools


class QuerySocketRealEstate:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((socket.gethostname(), 5000))
        self.delta_price = 10000
   
    
    def set_delta_money_range(self, delta):
        m = {'req' : 're_set_money', 'data': delta}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)

        return recDecoded['res']
    
    def next_money_range(self):
        m = {'req' : 're_next_money'}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)
        
        return recDecoded['res']

    def get_next_page(self):
        m = {'req' : 're_next_page'}
        data = json.dumps(m).encode('utf-8')

        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)

        return recDecoded['res']

    def get_query(self):
        m = {'req' : 're_get_query'}
        data = json.dumps(m).encode('utf-8')
        self.delta = 500
        self.sock.send(data)

        rec = self.sock.recv(1024)
        recDecoded = rec.decode('utf-8')
        recDecoded = json.loads(recDecoded)
            
        return recDecoded['res']