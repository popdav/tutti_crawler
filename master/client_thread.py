import json
from threading import Thread
from query_builder import QueryBuilder
# from query_builder_real_estate import QueryBuilderRealEstate

class ClientThread(Thread):

    def __init__(self, qq, address, sock=None):
        Thread.__init__(self)
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.addr = address
        self.qb = QueryBuilder('https://www.tutti.ch/api/v10/list.json?aggregated=1', 'https://www.tutti.ch/de/li/', qq)
        # self.qbre = QueryBuilderRealEstate('https://www.tutti.ch/api/v10/mapsearch/real_estate_search.json',
        #                       'https://www.tutti.ch/de/immobilien')

    def _get_query(self, req):
        if req['req'] == 'get_query':
            return self.qb.get_query()
        elif req['req'] == 'next_page':
            return self.qb.get_next_page()
        elif req['req'] == 'next_money':
            return self.qb.next_money_range()
        elif req['req'] == 'set_money':
            return self.qb.set_delta_money_range(int(req['data']))

        # elif req['req'] == 're_get_query':
        #     return self.qbre.get_query()
        # elif req['req'] == 're_next_page':
        #     return self.qbre.get_next_page()
        # elif req['req'] == 're_next_money':
        #     return self.qbre.next_money_range()
        # elif req['req'] == 're_next_area':
        #     return self.qbre.next_area_range()
        # elif req['req'] == 're_set_money':
        #     return self.qbre.set_delta_money_range(int(req['data']))
        # elif req['req'] == 're_set_area':
        #     return self.qbre.set_delta_area_range(int(req['data']))
        else:
            return None

    def run(self):
        
        while True:
            req = self.sock.recv(1024)
            reqDecoded = req.decode('utf-8')
            if reqDecoded == '':
                break
            reqJson = json.loads(reqDecoded)
            print(f'[Client {self.addr}] request: {reqJson}')
            query = self._get_query(reqJson)
            if query is None:
                print(f'[Client {self.addr}] bad request: {reqJson}')
                query = {'res': 'False', 'msg': 'Bad request'}
            res = json.dumps({'res': query}).encode('utf-8')
            sent = self.sock.send(res)
            if sent == 0:
                break

        print(f'[Client {self.addr}] disconnected')