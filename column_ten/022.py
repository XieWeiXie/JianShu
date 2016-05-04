"""
Get DoubanTop250 films
Crawl doubanTop250.
Author: wuxiaoshen
Date: 2016.05.04
__version__: V1.0
"""

# -*- coding:utf-8 -*-

import re
import requests
import MySQLdb
import lib
import pymongo
from pymongo import MongoClient


class DouBanTop(object):
    def __init__(self):
        self.url = "https://movie.douban.com/top250?start=0&filter="

        self.Film_pattern = r'<span class="title">(.*?)</span>'
        self.Director_pattern = r'<p class="">(.*?)</p>'
        self.Rates_pattern = r'<span class="rating_num" property="v:average">(.*?)</span>'
        self.Number_pattern_large = r'<div class="star">(.*?)</div>'
        self.Number_pattern_small = r'<span>(.*?)</span>'
        self.Describe_pattern = r'<span class="inq">(.*?)</span>'
        self.Urlfilm_pattern_large = r'<div class="hd">(.*?)</div>'
        self.Urlfilm_pattern_small = r'<a href="(.*?)"'

        pass

    def urls(self):
        Urls = []
        for page in range(0, 250,25):
            one = re.sub("start=\d+",'start=%s' % page, self.url,re.S)
            Urls.append(one)
            page += 1
        return Urls

        # another_urls = ["https://movie.douban.com/top250?start={}&filter=".format(i) for i in range(0,250,25)]
        # another_urls_two = ["https://movie.douban.com/top250?start=%s&filter=" % i for i in range(0, 250, 25)]
        # return another_urls
        # return another_urls_two
        pass

    def get_content(self, each_url):
        html = requests.get(each_url)
        try:
            if html.status_code == 200:
                response = html.text
                return response
        except:
            print("Can not connect to this website")
        pass

    def content_json(self, content):
        Film_all = re.findall(self.Film_pattern, content, re.S)
        Film = []
        for one_film in Film_all:
            if "&nbsp" not in one_film:
                Film.append(one_film)
        Director_all = re.findall(self.Director_pattern, content, re.S)
        Director = []
        for one_Director in Director_all:
            one = self.str_replace(one_Director)
            Director.append(one)
        Rates = re.findall(self.Rates_pattern, content, re.S)
        Number_large = re.findall(self.Number_pattern_large, content, re.S)
        Number = []
        for one_number in Number_large:
            Number_one = re.findall(self.Number_pattern_small, one_number, re.S)[0]
            Number.append(Number_one)
        Describe = re.findall(self.Describe_pattern, content, re.S)
        Url_largre = re.findall(self.Urlfilm_pattern_large, content, re.S)
        Url =[]
        for one_url in Url_largre:
            Url_one = re.findall(self.Urlfilm_pattern_small, one_url, re.S)[0]
            Url.append(Url_one)
        Film_collection = []
        for Film, Director, Rates, Number, Describe, Url in zip(Film, Director, Rates, Number, Describe, Url):
            data = {
                "Film": Film,
                "Director": Director,
                "Rates": Rates,
                "Number": Number,
                "Describe": Describe,
                "Url": Url
            }
            Film_collection.append(data)
        return Film_collection

    def str_replace(self, str_one):
        str_one_1 = str_one.replace("\n", '')
        str_one_2 = str_one_1.replace("<br>", '')
        str_one_3 = str_one_2.replace("&nbsp;", '')
        str_one_4 = str_one_3.replace("\t", "")
        str_one_5 = str_one_4.replace(" ", '').strip()
        return str_one_5

    def save_content(self, each_page_film_data, number=0):
        filename = "one\\"
        for each in each_page_film_data:
            f = open(filename + "%s.txt" % number,'wb')
            f.writelines('Film:' + each['Film'] + '\n')
            f.writelines('Director' + each['Director'] + '\n')
            f.writelines('Rates:' + each['Rates'] + '\n')
            f.writelines('Number:' + each['Number'] + '\n')
            f.writelines('Describe:' + each['Describe'] + '\n')
            f.writelines('Url:' + each['Url'] + '\n\n')
            number += 1
            f.close()

    def save_to_mysqldb(self, each_page_film_data, tablename):
        mysql = MySQLdb.connect(
            user="root",
            host="localhost",
            passwd="123456",
            port=3306,
            db='exercise',
            charset='utf8'
        )
        cursor = mysql.cursor()
        sql = lib.json_to_mysql(each_page_film_data,tablename)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            mysql.rollback()
        cursor.close()
        mysql.commit()
        mysql.close()
        pass

    def save_to_mongodb(self, each_page_film_data, tablename):
        client = pymongo.MongoClient()
        db = client.exercise
        result = db.tablename.insert(each_page_film_data)
        client.close()
        pass

    def select_from_mongodb(self):
        client = pymongo.MongoClient()
        db = client.exercise
        result = db.tablename.find()
        return result
        pass
    def save_by_sqlalchemy(self, each_page_film_data):
        pass



        pass

if __name__ == "__main__":
    url = "https://movie.douban.com/top250?start=0&filter="
    Start = DouBanTop()
    urls = Start.urls()
    for one_url in urls:
        one_page_content = Start.get_content(one_url)
        all_data = Start.content_json(one_page_content)
        for one in all_data:
            # Start.save_to_mysqldb(one, "douban_film")
            Start.save_to_mongodb(one,"table_name")
            pass
    A = Start.select_from_mongodb()
    for one in A:
        print(one)





