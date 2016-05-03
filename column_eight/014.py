# -*- coding: utf-8 -*-
# To: learn MySQldb
# Date: 2016/5/2
# Author: wuxiaoshen
import MySQLdb
class Transfer(object):
    def __init__(self, con):
        self.con = con
        pass

    def check_account(self, account_id):
        cur =  self.con.cursor()
        sql = 'select * from bank WHERE id ="%s"' % (str(account_id))
        cur.execute(sql)
        if cur.rowcount == 1:
            print("%s existes."%(account_id))
        else:
            print("%s is wrong" % account_id)


    def check_money(self, values, account_id):
        cur = self.con.cursor()
        sql = 'select * from bank WHERE id="%s" AND money>%s' % (account_id, values)
        cur.execute(sql)
        print(cur.rowcount)
        if cur.rowcount == 1:
            print("Enough money!")
            return True
        else:
            print("No enough money!")
            return False

    def subtract(self, accout_id, tranfer_money, Flag):
        cur = self.con.cursor()
        if Flag:
            try:
                sql = 'update bank SET money = money - %s where id = "%s"' % (tranfer_money, accout_id)
                cur.execute(sql)
                #print(cur.rowcount)
                if cur.rowcount == 1:
                    print(u"减款成功")
            finally:
                cur.close()
        else:
            print(u"操作不成功.")

    def add(self, accout_id, tranfer_money, Flag):
        cur = self.con.cursor()
        if Flag:
            try:
                sql = 'update bank SET money = money + %s WHERE id = "%s"' % (tranfer_money, accout_id)
                cur.execute(sql)
                #print(cur.rowcount)
                if cur.rowcount ==1:
                    print(u"加款成功")
            finally:
                cur.close()
        else:
            print(u"操作不成功.")
if __name__ == "__main__":
    connector = MySQLdb.connect(
        user="root",
        host="localhost",
        port=3306,
        passwd="123456",
        db="exercise",
        charset="utf8")
    Bank = Transfer(con=connector)
    try:
        Bank.check_account("zhangsan")
        Bank.check_account("lisi")
        Flag = Bank.check_money(100, "zhangsan")
        Bank.subtract("zhangsan", 100, Flag)
        Bank.add("lisi", 100, Flag)
        Bank.con.commit()
    except:
        connector.rollback()
    Bank.con.close()


