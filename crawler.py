import requests
from ProxiesPool.proxy import Proxy
from bs4 import BeautifulSoup
from utils import get_page


class Crawler(object):
    def __init__(self):
        pass

    '''
    :return: 返回类里所有crawl开头的方法名
    '''
    def get_methods(self):
        methods = []
        for method in dir(self):
            if "crawl_" in method:
                methods.append(method)
        return methods

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.%(func)s()" % {"func": callback}):
            print("成功获取代理：", proxy.ip)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self, page_count=5):   # 爬取快代理上的免费代理
        urls = ["https://www.kuaidaili.com/free/inha/{}".format(page) for page in range(1, page_count+1)]

        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                b = BeautifulSoup(html, "lxml")
                tr = b.find_all("tr")[1:]
                for td in tr:
                    ip = td.find_all("td")[0].text
                    port = td.find_all("td")[1].text
                    proxy_type = td.find_all("td")[3].text
                    # print("proxy: %(ip)s:%(port)s, type:%(type)s" % {"ip": ip, "port": port, "type": proxy_type})
                    proxy = Proxy(ip, port, proxy_type)
                    yield proxy

    def crawl_xicidaili(self, page_count=10):
        urls = ["http://www.xicidaili.com/nn/%s" % page for page in range(1, page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                b = BeautifulSoup(html, "lxml")
                trs = b.find_all("tr")[1:]
                for tr in trs:
                    ip = tr.find_all("td")[1].text
                    port = tr.find_all("td")[2].text
                    proxy_type = tr.find_all("td")[5].text
                    proxy = Proxy(ip, port, proxy_type)
                    yield proxy
            else:
                print(url, "____页面丢失！")


if __name__ == "__main__":
    c = Crawler()
    methods = c.get_methods()
    # for ip in c.crawl_kuaidaili():
    #     print(ip)
    for ip in c.crawl_xicidaili():
        print(ip.ip)

