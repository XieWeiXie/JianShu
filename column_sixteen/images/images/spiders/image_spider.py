# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from images.items import ImagesItem
from scrapy.selector import Selector

class Download(CrawlSpider):
    name = "image"
    allowed_domains = ["https://stocksnap.io/"]
    start_urls = ["https://stocksnap.io/",]

    def parse(self, response):
        print(response)
        hxs = Selector(response)
        imgs = hxs.xpath('//div[@class="photo-item"]//img/@src').extract()
        item = ImagesItem()
        item['image_urls']=imgs
        return item

