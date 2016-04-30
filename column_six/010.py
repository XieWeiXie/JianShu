# -*- coding: utf-8 -*-
# Date:2016.04.30
# To: crawl blog
# Author: wuxiaoshen

import requests
from bs4 import BeautifulSoup
import re
import codecs

class Blog(object):

    def __init__(self):
        self.url = "http://xlzd.me/"
        self.all_url = []
        global name
        name = 1

        pass

    def search_url_one(self):
        self.all_url = ["http://xlzd.me/page/{}/".format(i) for i in range(1, 8)]
        return self.all_url
        pass

    def search_url_two(self):
        for one in range(1, 8):
            url = "http://xlzd.me/page/" + str(one) + '/'
            self.all_url.append(url)
        return self.all_url
        pass

    def contents(self, url):
        html = requests.get(url)
        response = html.text
        Soup = BeautifulSoup(response, "lxml", from_encoding="utf-8")
        all_title = Soup.find_all(class_="post-title")
        all_abstract = Soup.find_all(class_="post-content")
        passage_urls = []
        passage_title = []
        passage_abstract = []
        for one_title in all_title:
            passage_urls.append(one_title.a.get('href'))
            passage_title.append(one_title.get_text())
        for one_abstract in all_abstract:
            passage_abstract.append(one_abstract.get_text())
        All = []
        for passage_urls, passage_title, passage_abstract in zip(passage_urls,passage_title,passage_abstract):
            data = \
                {"url": passage_urls,
                 "title": passage_title,
                 "abstract": passage_abstract}
            All.append(data)
        return All

    def save(self, passage):
        global name
        for one in range(len(passage)):
            with codecs.open("Blog\\" + str(name) + ".txt", 'wb', encoding='utf-8') as f:
                f.write(passage[one]["url"])
                f.write("\n")
                f.write(passage[one]["title"])
                f.write("\n")
                f.write(passage[one]["abstract"])
                f.write("\n")
                name +=1

                pass

        pass

if __name__ == "__main__":
    Spider = Blog()
    all_url = Spider.search_url_one()
    for one_url in all_url:
        one_content = Spider.contents(one_url)
        Spider.save(one_content)
        pass