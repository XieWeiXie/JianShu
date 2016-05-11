# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from Liuweipeng.items import LiuweipengItem

class BlogSpider(Spider):
    name = "liuweipeng"
    start_urls = ["http://mindhacks.cn/","http://mindhacks.cn/page/2/", "http://mindhacks.cn/page/3/", "http://mindhacks.cn/page/4/"]
    def parse(self, response):
        url_item = []
        selector = Selector(response)
        each_page_data = selector.xpath('//div[@id="index-featured1"]/ul/li/h3[@class="entry-title"]/a/@href').extract()
        each_page_data_other = selector.xpath('//div[@id="content"]/div/ul/li/h3[@class="entry-title"]/a/@href').extract()
        url_item.extend(each_page_data)
        url_item.extend(each_page_data_other)
        for one in url_item:
            yield Request(one, callback=self.parse_detail)

    def parse_detail(self, response):
        Item = LiuweipengItem()
        selector = Selector(response)
        title = selector.xpath('//div[@id="content"]/div/h1[@class="entry-title"]/a/text()').extract()
        time = selector.xpath('//div[@id="content"]/div/div[@class="entry-info"]/abbr/text()').extract()
        content = selector.xpath('//div[@id="content"]/div/div[@class="entry-content clearfix"]/p/text()').extract()
        url = selector.xpath('//div[@id="content"]/div/h1[@class="entry-title"]/a/@href').extract()
        print(content)
        for title, time, content, url in zip(title, time, content, url):
            Item["Title"] = title
            Item["Time"] = time
            Item["Content"] = content
            Item["Url"] = url
        yield Item

