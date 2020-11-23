from scrapers.tutti_scraper import Tutti
from scrapers.tutti_real_estate_scraper import TuttiRealEstate
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from datetime import datetime
import sys, os, tarfile

class CrawlerMain():
    def __init__(self):
        self.s = get_project_settings()
        self.s['USER_AGENTS'] = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36']
        # self.s['DOWNLOAD_DELAY'] = 0.5
        self.s['DOWNLOADER_MIDDLEWARES'] = {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
        self.s['COOKIES_ENABLED'] = True
        self.s['COOKIES_DEBUG'] = True
        self.s['SPLASH_URL'] = 'http://192.168.59.103:8050'

        self.s['SPIDER_MIDDLEWARES'] = {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        }
        self.s['DUPEFILTER_CLASS'] = 'scrapy_splash.SplashAwareDupeFilter'
        self.s['HTTPCACHE_STORAGE'] = 'scrapy_splash.SplashAwareFSCacheStorage'

    def start(self):
        data_path = './data/data.json' #path were tu save data crawled

        f = open(data_path, 'w+')
        f.write('[\n')
        f.close()
        
        process = CrawlerProcess(self.s)
        process.crawl(Tutti)
        process.start()

        with open(data_path, 'rb+') as filehandle:
            filehandle.seek(-2, os.SEEK_END)
            filehandle.truncate()
    
        f = open(data_path, 'a+')
        f.write('\n]')
        f.close()

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        nameTar = f'data-{timestamp}'
        dataTar = tarfile.open(nameTar+'.tar.gz', 'w:gz')
        dataTar.add('./data', arcname=nameTar)
        dataTar.close()

if __name__ == "__main__":
    cm = CrawlerMain()
    cm.start()