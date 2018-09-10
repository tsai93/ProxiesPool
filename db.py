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
                cursor.execute(sql)
                data = cursor.fetchall()
                self.db.commit()
                print(data)
            else:
                print("该代理ip已存在……")

    '''
    随机取出一条代理
    '''
    def random(self, type='HTTPS'):
        sql = 'SELECT proxy_ip, proxy_port, proxy_type, proxy_score FROM proxies AS t1 JOIN ( SELECT (ROUND( RAND( ) * ( SELECT MAX( proxy_id ) - MIN( proxy_id ) FROM proxies ) ) + (SELECT MIN(proxy_id) FROM proxies)) AS id ) AS t2 WHERE t1.proxy_id = t2.id AND t1.proxy_score = (SELECT MAX(proxy_score) FROM proxies) LIMIT 1'
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) != 0:
            print(data)
        else:
            self.random()

    '''
    分数直接增加到100
    '''
    def increase(self, proxy):
        pass

    '''
    扣1分
    '''
    def decrease(self, proxy):
        pass

    '''
    低于60直接删除
    '''
    def delete(self, proxy):
        pass


# p = {'ip': '36.99.206.26', 'port': '22172', 'type': 'HTTPS'}
# a = {}
# pro = Proxy(p['ip'], p['port'], p['type'])
# print(pro.ip)
# m = MySQLClient()
# m.add(pro)
m = MySQLClient()
# ps = Crawler()
# for p in ps.crawl_xicidaili():
#     m.add(p)
m.random()