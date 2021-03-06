import scrapy
import math , json, sys
sys.path.insert(1, './services/')
from query_socket import QuerySocket



class Tutti(scrapy.Spider):

    def __init__(self, **kwargs):
        super().__init__(name='tutti',**kwargs)
        self.name = 'tutti'
        self.allowed_domains = ['tutti.ch']
        self.qs = QuerySocket()
        self.urls = self.qs.get_query()
        self.start_urls = [ self.urls['http'] ]
        self.tutti_token = ''

    def parse(self, response):

        self.tutti_token = response.xpath('//meta[@name="msvalidate.01"]/@content').get()
        
        headers = {
            'X-Tutti-Hash': self.tutti_token
        }
        
        yield scrapy.Request(
                response.urljoin(self.urls['api']),
                callback=self.parse_tutti_list,
                dont_filter=True,
                headers=headers
            )

    def parse_tutti_list(self, response):
        json_body = json.loads(response.body.decode("utf-8"))

        headers = {
            'X-Tutti-Hash': self.tutti_token
        }

        if int(json_body['search_total']) == 0:
            self.urls = self.qs.get_query()
            
            if self.urls == '':
                return

            yield scrapy.Request(
                response.urljoin(self.urls['api']),
                callback=self.parse_tutti_list,
                dont_filter=True,
                headers=headers
            )

        elif int(json_body['search_total']) <= 3000:
            for item in json_body["items"]:
                yield scrapy.Request(
                    response.urljoin(f'https://www.tutti.ch/api/v10/item/view.json?item_id={item["id"]}'),
                    callback=self.parse_tutti_item,
                    dont_filter=True,
                    headers=headers
                )

            self.urls = self.qs.get_next_page()

            if self.urls == '':
                self.urls = self.qs.next_money_range()
            print(f'NEXT URL: {self.urls["api"]}')
            yield scrapy.Request(
                response.urljoin(self.urls['api']),
                callback=self.parse_tutti_list,
                dont_filter=True,
                headers=headers
            )
        else:
            self.urls = self.qs.set_delta_money_range(self.qs.delta/2)
            yield scrapy.Request(
                response.urljoin(self.urls['api']),
                callback=self.parse_tutti_list,
                dont_filter=True,
                headers=headers
            )

    def parse_tutti_item(self, response):
        json_body = json.loads(response.body.decode("utf-8"))
        f = open('./data/data.json', 'a+')
        f.write(json.dumps(json_body))
        f.write(',\n')
        f.close()


    