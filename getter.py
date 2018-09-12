from ProxiesPool.crawler import Crawler
from ProxiesPool.db import MySQLClient


class Getter(object):
    def __init__(self):
        self.crawler = Crawler()
        self.db = MySQLClient()

    def run(self):
        if not self.db.is_over_threshold():
            for method in self.crawler.get_methods():
                for proxy in self.crawler.get_proxies(callback=method):
                    self.db.add(proxy)
        else:
            print("Pool is overflow")


if __name__ == "__main__":
    g = Getter()
    g.run()