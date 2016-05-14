# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from lib import Article
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
class LiuweipengPipeline(object):
    # def __init__(self):
    #     host = settings['MONGODB_HOST']
    #     port = settings['MONGODB_PORT']
    #     dbName = settings['MONGODB_DBNAME']
    #     client = pymongo.MongoClient(host=host, port=port)
    #     tdb = client[dbName]
    #     self.post = tdb[settings['MONGODB_DOCNAME']]
    # def process_item(self, item, spider):
    #     content = dict(item)
    #     self.post.insert(content)
    # def __init__(self):
    #     self.connection = pymysql.connect(host='localhost',
    #                          user='root',
    #                          password='123456',
    #                          port=3306,
    #                          db='test',
    #                          charset='utf8')
    #     pass
    # def process_item(self, item, spider):
    #     with self.connection.cursor() as cursor:
    #         sql = "INSERT INTO `blog_2`(`Title`, `Time`, `Content`, `Url`) VALUES (%s, %s, %s, %s)"
    #         cursor.execute(sql, (item['Title'],item["Time"], item["Content"],item["Url"]))
    #     self.connection.commit()

    def open_spider(self, spider):
        engine = create_engine("mysql://root:123456@localhost:3306/test?charset=utf8", echo = True)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        pass

    def process_item(self, item, spider):
        one = Article(Title=item["Title"],
                    Time=item["Time"],
                    Content=item["Content"],
                    Url=item["Url"])
        self.session.add(one)

        pass
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
        pass
