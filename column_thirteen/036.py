# -*- coding:utf-8 -*-
# To: learn selenium, PhantomJS and sqlalchemy
# Date: 2016.05.10
__author__ = "wuxiaoshen"

import unittest
from selenium import webdriver
from lxml import etree
from sqlalchemy import create_engine
from sqlalchemy import Column, String,Table, MetaData,Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base

class seleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def testchinamovie(self):
        driver = self.driver
        driver.get("http://www.cbooo.cn/")
        selector = etree.HTML(driver.page_source)
        Ranks = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[1]/text()')
        Movienames = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[2]/text()')
        Realtimes = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[3]/text()')
        Ratio_of_movies = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[4]/text()')
        sum_movies = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[5]/text()')
        Ration_of_opens = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[6]/text()')
        Screen_times = selector.xpath('//div[@id="top_list"]/table/tbody/tr/td[7]/text()')
        Movie_datas = []
        print(Ranks)
        for Rank, Moviename, Realtime, Ratio_of_movie, sum_movie, Ration_of_open, Screen_time in zip(Ranks, Movienames, Realtimes, Ratio_of_movies, sum_movies, Ration_of_opens, Screen_times):
            data = {"Rank": Rank,
                    "Moviename": Moviename,
                    "Realtime": Realtime,
                    "Ratio_of_movie": Ratio_of_movie,
                    "sum_movie": sum_movie,
                    "Ration_of_open": Ration_of_open,
                    "Screen_time": Screen_time}
            print(data)
            Movie_datas.append(data)
        #print (Movie_datas)
        engine = create_engine("mysql://root:123456@localhost:3306/test?charset=utf8", echo = True)
        Base = declarative_base()
        metadata = MetaData(engine)
        sql_table = Table("Realtime_film", metadata,
                          Column("id", Integer, primary_key=True),
                          Column("Rank", String(32)),
                          Column("Moviename", String(32)),
                          Column("Realtime", String(12)),
                          Column("Ratio_of_movie", String(16)),
                          Column("sum_movie", String(128)),
                          Column("Ration_of_open", String(128)),
                          Column("Screen_time", String(128)),
                            mysql_engine='InnoDB',
                            mysql_charset='utf8')
        sql_table.create()
        sql_table_2 = Table("Realtime_film", metadata, autoload=True)
        i = sql_table_2.insert()
        # for one in Movie_datas:
        #     i.execute(one)
        con = engine.connect()
        con.execute(i, Movie_datas)
    def tearDown(self):
        self.driver.close()
if __name__=="__main__":
    unittest.main()