FROM python:3.7

WORKDIR /slave

RUN pip3 install scrapy scrapy_useragents scrapy_splash

COPY . /slave

CMD [ "python3", "crawler_main.py" ]