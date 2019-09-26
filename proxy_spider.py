# -*- coding: UTF-8 -*-
import telnetlib

import requests
from fake_useragent import UserAgent

import settings
from parse_data import XICIParse
from save_data import SaveData


class ProxySpider(object):
    """ip代理爬取"""

    def __init__(self, url, proxy=None):
        self.url = url
        self.page = 1
        self.proxy = proxy

    def get_url(self):
        """初始化url"""
        return self.url.format(self.page)

    def get_response(self, url):
        """发送request请求获取网页源码数据"""
        try:
            headers = {"User-Agent": UserAgent(verify_ssl=False).random}
            response = requests.get(url, headers=headers)
            return response.content.decode()
        except:
            print("获取数据错误")
            return None

    def parse(self, data):
        """提取数据"""
        xici = XICIParse(data)
        result = xici.parse()
        return result

    def check_ip(self, proxy_list):
        """检测ip"""
        result = []
        for proxy_ip in proxy_list:
            try:
                telnetlib.Telnet(proxy_ip["ip"], proxy_ip["port"], timeout=1)
            except:
                print(proxy_ip, "无法使用")
            else:
                print(proxy_ip, "可以使用")
                result.append(proxy_ip)
        return result

    def save(self, data):
        """保存数据到数据库中"""
        save_data = SaveData(data)
        save_data.save()

    def run(self):
        while True:
            # 1.初始化请求
            url = self.get_url()

            # 2.发送请求 获取相应
            response_html = self.get_response(url)

            if response_html is not None:
                # 3.获取数据
                data = self.parse(response_html)

                if data is not None:
                    # 监测ip是否可用
                    result = self.check_ip(data)
                    self.save(result)
                else:
                    break
            else:
                break
            self.page += 1


if __name__ == '__main__':
    url = settings.XICIURL
    p = ProxySpider(url)
    p.run()
