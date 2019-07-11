#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from helper.logger import Logger
from helper.extras import parser, get_html, save_proxy, proxy_checker


class Proxy_list:
    def __init__(self):
        self.baseUrl = 'https://www.free-proxy-list.net/'
        self.logger = Logger(name=self.__class__.__name__)
        self.selector = {
            'table': '#list',
            'item': 'tr:has("td")',
            'ip': 'td:nth-child(1)',
            'port': 'td:nth-child(2)',
            'type': 'td:nth-child(7)',
        }

    def proxy_parser(self, html):
        result = []
        try:
            table = parser(html, self.selector['table'])
            raw_content = parser(table, self.selector['item'])
            if raw_content:
                proxys = raw_content.remove('.active')
                for proxy in proxys:
                    tmp = dict()
                    ip = parser(proxy, self.selector['ip']).text()
                    port = parser(proxy, self.selector['port']).text()
                    type = parser(proxy, self.selector['type']).text().lower()
                    if type == 'yes':
                        tmp['address'] = ip
                        tmp['port'] = port
                        result.append(tmp)
        except Exception as e:
            self.logger.log(str(e), level='error')
        return result

    def main(self, path):
        html = get_html(Proxy_list().baseUrl)
        checker = self.proxy_parser(html)
        self.logger.log('get {} proxies'.format(len(checker)))
        save_proxy(proxies=proxy_checker(checker), location=path)
