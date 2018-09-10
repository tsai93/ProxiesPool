MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PWD = 'caiheming'
MYSQL_DB = 'testdb'
import pymysql


class MySqlHelper(object):
    def __init__(self):
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB)
        self.sql = ''
    def add(self, dict):
        pass

dic = {'a': '1', 'b':'2'}
for d in dic:
    print(dic[d])