from helper.logger import Logger
from helper.extras import get_html, parser, proxy_checker, save_proxy

class Spys:
    def __init__(self):
        self.baseUrl = 'http://spys.one/en/https-ssl-proxy/'
        self.logger = Logger(name=self.__class__.__name__)
        self.payload = "xpp=2&xf1=0&xf4=2&xf5=0"
        self.headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }
        self.selector = {
            'table': 'tr[onmouseover*="this"] td[colspan="1"]:nth-child(1)',
            'ip': 'font.spy14',
            'port': 'font.spy14 font'
        }

    def proxy_parser(self, html):
        ip = port = ''
        result = []
        try:
            tables = parser(html, self.selector['table'])
            for table in tables:
                ip = parser(table, self.selector['ip']).remove('script').text()
                port = 8080
                result.append({'address':ip, 'port':port})
        except Exception as e:
            self.logger.log(msg=str(e), level='error')
        return result


    def main(self):
        html = get_html(self.baseUrl, headers=self.headers, payloads=self.payload)
        checker  = self.proxy_parser(html)
        self.logger.log('get {} proxies'.format(len(checker)))
        proxies = proxy_checker(proxys=checker)
        save_proxy(proxies, type='https')

