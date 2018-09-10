import pymysql
from random import choice
from ProxyPool.proxy import Proxy
from ProxyPool.crawler import Crawler

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
                cursor.execute(sql)
                data = cursor.fetchall()
                self.db.commit()
                print(data)
            else:
                print("该代理ip已存在……")


# p = {'ip': '36.99.206.26', 'port': '22172', 'type': 'HTTPS'}
# a = {}
# pro = Proxy(p['ip'], p['port'], p['type'])
# print(pro.ip)
# m = MySQLClient()
# m.add(pro)
m = MySQLClient()
ps = Crawler()
for p in ps.crawl_xicidaili():
    m.add(p)