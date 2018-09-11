import pymysql
from random import choice
from ProxiesPool.proxy import Proxy
from ProxiesPool.crawler import Crawler

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PWD = 'caiheming'
MYSQL_DB = 'testdb'


class MySQLClient(object):
    def __init__(self):
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB)

    def test(self):
        cursor = self.db.cursor()
        sql = r'select * from proxies'
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
    '''
    将代理写入Mysql
    '''
    def add(self, proxy):
        if isinstance(proxy, Proxy):
            sql = 'select * from proxies where proxy_ip = "%s"' % proxy.ip
            print(sql)
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print(data)
                sql = 'insert INTO proxies (proxy_ip , proxy_port , proxy_type, proxy_score) VALUES ("%(ip)s", "%(port)s", "%(type)s", %(score)d)' % {"ip": proxy.ip, "port": proxy.port, "type": proxy.type, "score": INITIAL_SCORE}
                try:
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    self.db.commit()
                except:
                    self.db.rollback()
                self.db.close()
            else:
                print("代理:%s已存在……" % (":".join([proxy.ip, proxy.port])))

    '''
    随机取出一条代理
    :return: Proxy类
    '''
    def random(self, proxy_type='HTTPS'):
        proxy_type = proxy_type.upper()
        if proxy_type != "HTTP" and proxy_type != "HTTPS":
            print("请求代理类型错误！")
        else:
            sql = 'SELECT * FROM proxies as t1 JOIN (SELECT ROUND(RAND() * (SELECT MAX(proxy_id) - MIN(proxy_id) FROM proxies) + (SELECT MIN(proxy_id) FROM proxies)) as id) as t2 WHERE t1.proxy_type = "%s" AND t1.proxy_id > t2.id LIMIT 1' % proxy_type
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if len(data) == 0:
                print("数据库中没有%s类型的代理服务器了" % proxy_type)
            print(data)
            proxy = Proxy(ip=data[1], port=data[2], type=data[3])
            return proxy

    '''
    分数直接增加到100
    '''
    def increase(self, proxy):
        if isinstance(proxy, Proxy):
            if self.isExist(proxy):
                ip = proxy.ip
                sql = 'update proxies set proxy_score = 100 where proxy_ip="%s"' % ip
                cursor = self.db.cursor()
                try:
                    cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()
                self.db.close()

    '''
    扣1分
    '''
    def decrease(self, proxy):
        if isinstance(proxy, Proxy):
            ip = proxy.ip
            sql = 'select * from proxies where proxy_ip="%s"' % ip
            cursor = self.db.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if len(data) != 0:

                score = data[4]
                sql = 'update proxies set proxy_score=%s where proxy_ip= "%s"' % (int(score) - 1, ip)
                try:
                    cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()
                self.db.close()

    '''
    低于60直接删除
    '''
    def delete(self, proxy):
        if isinstance(proxy, Proxy):
            if self.isExist(proxy):
                ip = proxy.ip
                sql = 'delete from proxies where proxy_ip="%s"' % ip
                cursor = self.db.cursor()
                try:
                    cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()
                self.db.close()


    def isExist(self, proxy):
        ip = proxy.ip
        sql = 'select * from proxies where proxy_ip="%s"' % ip
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if len(data) != 0:
            return True
        else:
            return False
# p = {'ip': '36.99.206.26', 'port': '22172', 'type': 'HTTPS'}
# a = {}
# pro = Proxy(p['ip'], p['port'], p['type'])
# print(pro.ip)
# m = MySQLClient()
# m.add(pro)
m = MySQLClient()
# ps = Crawler()
# for p in ps.crawl_kuaidaili():
#     m.add(p)
m.increase(m.random(proxy_type='http'))