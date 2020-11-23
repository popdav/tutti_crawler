import json, os, re
import itertools

class QueryQueue:

    def __init__(self):
        self._load_json()
        self._get_values()
        self._init_values()
        
    def _init_values(self):
        self.permutation_iter = 0
        


    def _load_json(self):
        current_dir = os.getcwd()
        file_categories = open(current_dir+'/query_data/categories.json', 'r')
        file_company_ad = open(current_dir + '/query_data/company_ad.json', 'r')
        file_region = open(current_dir + '/query_data/region.json', 'r')
        file_type = open(current_dir + '/query_data/type.json', 'r')
        file_lang = open(current_dir + '/query_data/lang.json', 'r')
        
        
        self.categories = json.load(file_categories)
        self.company_ads = json.load(file_company_ad)
        self.regions = json.load(file_region)
        self.types = json.load(file_type)
        self.languages = json.load(file_lang)
        
        file_categories.close()
        file_company_ad.close()
        file_region.close()
        file_type.close()
        file_lang.close()

    def _get_values(self):
        self.category_values = []
        self.company_ads_values = []
        self.region_values = []
        self.type_values = []
        self.lang_values = []

        self._get_category_values()
        self._get_company_ads_values()
        self._get_region_values()
        self._get_type_values()
        self._get_lang_values()

        self._calc_permutations()

    def _get_category_values(self):
        for category in self.categories:
            if category['children'] is not None:
                for child in category['children']:
                    if re.search('^10', child['value']) is None:
                        self.category_values.append(child['value'])
            else:
                if re.search('^10', category['value']) is None:
                    self.category_values.append(category['value'])

    def _get_company_ads_values(self):
        for ad in self.company_ads:
            ad_view = ad.values()
            ad_iterator = iter(ad_view)
            first_val = next(ad_iterator)
            self.company_ads_values.append(first_val)

    def _get_region_values(self):
        for region in self.regions:
            region_view = region.values()
            region_iter = iter(region_view)
            first_val = next(region_iter)
            self.region_values.append(first_val)

    def _get_type_values(self):
        for typeA in self.types:
            type_view = typeA.values()
            type_iter = iter(type_view)
            first_val = next(type_iter)
            self.type_values.append(first_val)

    def _get_lang_values(self):
        for lang in self.languages:
            lang_view = lang.values()
            lang_iter = iter(lang_view)
            first_val = next(lang_iter)
            self.lang_values.append(first_val)

    def _calc_permutations(self):
        self.premutations = list(itertools.product(self.category_values, self.company_ads_values, self.region_values, self.type_values, self.lang_values))
    

    def _get_region_value(self, region_id):
        for region in self.regions:
            for key in region.keys():
                if region[key] == region_id:
                    return key.lower()
    
    def _get_type_value(self, type_val):
        for tp in self.types:
            for key in tp.keys():
                if tp[key] == type_val:
                    return key.lower()

    def _get_category_value(self, category_id):
        for category in self.categories:
            if category["value"] == category_id:
                text = category["text"]["de"].lower()
                text = re.sub('*\s\&\s*', '-', text)
                text = re.sub('*\s*', '-', text)
                return text

            for child in category["children"]:
                if child["value"] == category_id:
                    text_parent = category["text"]["de"].lower()
                    text_parent = re.sub('\s\&\s', '-', text_parent)
                    text_parent = re.sub('\s', '-', text_parent)

                    text_child = child["text"]["de"].lower()
                    text_child = re.sub('\s\&\s', '-', text_child)
                    text_child = re.sub('\s', '-', text_child)
                    
                    return text_parent + "/" + text_child

    def _get_parent_category(self, child_category):
        for category in self.categories:
            for child in category["children"]:
                if child["value"] == child_category:
                    return category["value"]

        return None

    def next_permutation(self):
        if self.permutation_iter >= len(self.premutations):
            return False

        perm = self.premutations[self.permutation_iter]
        self.permutation_iter += 1
        
        return perm