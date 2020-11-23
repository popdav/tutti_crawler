import json, os, re
import itertools

#https://www.tutti.ch/api/v10/mapsearch/real_estate_search.json

class QueryBuilder:

    def __init__(self, base_api, base_http, qq):
        self.query_queue = qq
        self.base_url = base_api
        self.base_http = base_http
        self._init_values()

    def _init_values(self):
        self.page = 1
        self.limit = 30
        self.with_all_regions = "false"
        self.ps = 0
        self.pe = 500
        self.delta = 500
        self.perm = False

    def _next_permutation(self):
        self.perm = self.query_queue.next_permutation()
        if not self.perm:
            return False

        self.category = self.perm[0]
        self.company_ad = self.perm[1]
        self.region = self.perm[2]
        self.typeA = self.perm[3]
        self.lang = self.perm[4]

        self.page = 1
        self.ps = 0
        self.pe = 500
        self.delta = 500

        return True

    def _query_build(self):
        parent_category = self.query_queue._get_parent_category(self.category)
        if parent_category is None:
            query_api = f'&category={self.category}&company_ad={self.company_ad}&' \
                    f'limit={self.limit}&o={self.page}&pe={self.pe}&ps={self.ps}&' \
                    f'query_lang={self.lang}&region={self.region}&st={self.typeA}&with_all_regions={self.with_all_regions}'
        else:
            query_api = f'&category={parent_category}&company_ad={self.company_ad}&' \
                    f'limit={self.limit}&o={self.page}&pe={self.pe}&ps={self.ps}&' \
                    f'query_lang={self.lang}&region={self.region}&st={self.typeA}&subcategory={self.category}&' \
                    f'with_all_regions={self.with_all_regions}'

        query_http = f'{self.query_queue._get_region_value(self.region)}/' \
                    f'{self.query_queue._get_type_value(self.typeA)}/' \
                    f'{self.query_queue._get_category_value(self.category)}' \
                    f'?company_ad={self.company_ad}&pe={self.pe}&ps={self.ps}&query_lang={self.lang}'
        
        query_body = {
            "http": self.base_http + query_http,
            "api": self.base_url + query_api
        }
        return query_body

    def set_delta_money_range(self, delta):
        self.ps = 0
        self.pe = delta
        self.delta = delta

        return self._query_build()
    
    def next_money_range(self):
        self.ps += self.delta
        self.pe += self.delta
        self.page = 1
        return self._query_build()

    def get_next_page(self):
        self.page += 1
        if self.page == 101:
            return ''

        query = self._query_build()

        return query

    def get_query(self):
        permutation_not_out_of_range =self._next_permutation()
        if not permutation_not_out_of_range:
            return ''

        query = self._query_build()   

        return query
