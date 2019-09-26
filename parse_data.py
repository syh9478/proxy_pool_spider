# -*- coding: UTF-8 -*-
from lxml import etree


class XICIParse(object):
    """提取西刺的ip代理"""

    def __init__(self, html):
        self.element = etree.HTML(html)

    def parse(self):
        """提取数据"""
        ip_list = []
        tr_list = self.element.xpath("//table[@id='ip_list']/tr")[1:]
        for tr in tr_list:
            item = {}
            item["ip"] = tr.xpath(".//td[2]/text()")[0]
            item["port"] = tr.xpath(".//td[3]/text()")[0]
            item["agent_form"] = tr.xpath(".//td[6]/text()")[0]
            ip_list.append(item)
        return ip_list
