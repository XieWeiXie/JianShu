# -*- coding: utf-8 -*-
# To: dangdang book in psychology
# Date: 2016/5/1
# Author: wuxiaoshen

import requests
import codecs
import re
import pymongo
from lxml import etree


class DangdangBook(object):

    def __init__(self):
        self.url_root = "http://category.dangdang.com/pg1-cp01.31.00.00.00.00.html"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
                        "Referer": "http://cm.ipinyou.com/cma_dangdang.html"}
        # re
        self.Bookname_pattern = r'<p class="name" ><a title="(.*?)"'
        self.Star_pattern = r'name="P_pl">(.*?)<'
        self.Writer_pattern_large = r'<p class="author">(.*?)</p>'
        self.Writer_pattern = r"name='P_zz' title='.*?'>(.*?)</a>"
        self.Time_pattern = r'class="publishing_time"><span></span>/(.*?)</p>'
        self.Publish_pattern = r"name='P_cbs'\stitle='(.*?)'>"
        self.Detail_pattern = r'<p class="detail" >(.*?)</p>'
        self.Price_n_pattern = r'<p class="price" > <span class="price_n">&yen;(.*?)</span>'
        self.Price_r_pattern = r'<span class="price_r">&yen;(.*?)</span>'
        self.Url_pattern = r'class="pic"  href="(.*?)"'

        # xpath
        self.Bookname_pattern_3 = r"//li/div/a/@title"
        self.Star_pattern_3 = r'//p[@class="star"]/a/text()'
        self.Writer_pattern_3 = r'//div[@class="publisher_info"]/p[@class="author"]/a[1]//@title'
        self.Time_pattern_3 = r'//div[@class="publisher_info"]/p[@class="publishing_time"]/text()'
        self.Publish_pattern_3 = r'//div[@class="publisher_info"]/p[@class="publishing"]/a[1]/text()'
        self.Detail_pattern_3 = r'//p[@class="detail"]/text()'
        self.Price_n_pattern_3 = r'//div[@class="inner"]/p[@class="price"]/span[@class="price_n"]/text()'
        self.Price_r_pattern_3 = r'//div[@class="inner"]/p[@class="price"]/span[@class="price_r"]/text()'
        self.Url_pattern_3 = r'//div[@class="inner"]/a//@href'

        pass

    def urls(self):
        all_urls = ["http://category.dangdang.com/pg{}-cp01.31.00.00.00.00.html".format(i) for i in range(1, 101, 1)]
        return all_urls
        pass

    def contents_re(self, one_url):
        html = requests.get(one_url, headers=self.headers)
        if html.status_code != 200:
            return -1
        else:
            response = html.text
        # print(response)
        selector = etree.HTML(response)
        Booksname = re.findall(self.Bookname_pattern, response, re.S)
        Stars = re.findall(self.Star_pattern, response, re.S)
        Writers = selector.xpath('//div/p[@class="author"]/a[1]/text()')
        Publishs = re.findall(self.Publish_pattern, response, re.S)
        Details_large = re.findall(self.Detail_pattern, response, re.S)
        Details = []
        for one in Details_large:
            one.strip("")
            one = one.replace("\n", "")
            one = one.replace(" ", "")
            one = one.replace("\u3000", "")
            one = one.replace("\t", '')
            one = one.replace("&nbsp;", '')
            Details.append(one)
        Price_ns = re.findall(self.Price_n_pattern, response, re.S)
        Price_rs = re.findall(self.Price_r_pattern, response, re.S)
        Urls = re.findall(self.Url_pattern, response, re.S)
        All_data = []
        for Booksname, Stars, Writers, Publishs, Details, Price_ns, Price_rs, Urls in zip(Booksname, Stars, Writers, Publishs, Details, Price_ns, Price_rs, Urls):
            data = {
                "Book": Booksname,
                "Star": Stars,
                "Writer": Writers,
                "Publish": Publishs,
                "Detail": Details,
                "Price_1": Price_rs,
                "Price_2": Price_ns,
                "Url": Urls

            }
            All_data.append(data)
        return All_data

    def contents_bs4(self):

        pass

    def contents_xpath(self, one_url):
        html = requests.get(one_url, headers=self.headers)
        if html.status_code != 200:
            return -1
        else:
            response = html.text
        selector = etree.HTML(response)
        booknames = selector.xpath(self.Bookname_pattern_3)
        writers = selector.xpath(self.Writer_pattern_3)
        time = selector.xpath(self.Time_pattern_3)
        stars = selector.xpath(self.Star_pattern_3)
        details = selector.xpath(self.Detail_pattern_3)
        price_n = selector.xpath(self.Price_n_pattern_3)
        price_r = selector.xpath(self.Price_r_pattern_3)
        urls = selector.xpath(self.Url_pattern_3)
        All_data = []
        for booknames, writers, time, stars, details, price_n, price_r, urls in zip(booknames, writers, time, stars, details, price_n, price_r, urls):
            data = {
                "bookname": booknames,
                "writers": writers,
                "stars": stars,
                "details": details,
                "price_n": price_n,
                "price_r": price_r,
                "urls": urls
            }
            All_data.append(data)
        return All_data

        pass

    def save_text(self, book_infos, page):
        global info
        info = 1
        for one in book_infos:
            with codecs.open("DangDang\\book_info_{}.txt".format(page), 'a+', encoding="utf-8") as f:
                f.write("Book" + str(info))
                f.write("\n")
                f.write(u"书名: " + one["bookname"])
                f.write("\n")
                f.write(u"作者: " + one["writers"])
                f.write("\n")
                f.write(u"评价人数: " + one["stars"])
                f.write("\n")
                f.write(u"简介: " + one["details"])
                f.write("\n")
                f.write(u"售价: " + one["price_n"])
                f.write("\n")
                f.write(u"定价: " + one["price_r"])
                f.write("\n")
                f.write(u"书籍链接: " + one["urls"])
                f.write("\n")
                info +=1



        pass

    def save_mysql(self):

        pass

    def save_mongodb(self, one_content):
        client = pymongo.MongoClient()
        db = client.dangdang
        result = db.dangdang.insert_many(one_content)
        client.close()

        pass


if __name__ == "__main__":
    url_root = "http://category.dangdang.com/pg1-cp01.31.00.00.00.00.html"
    DD = DangdangBook()
    All_data = DD.contents_xpath(url_root)
    DD.save_text(All_data, 1)
