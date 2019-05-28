import os
import requests
from helper.extras import save_proxy, proxy_checker
from helper.logger import Logger

current_path = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_path, os.pardir)

class Hidester:
    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__)

    def get_data(self):
        results = None
        try:
            url = "https://hidester.com/proxydata/php/data.php"
            querystring = {"mykey": "data", "offset": "0", "limit": "500", "orderBy": "latest_check",
                           "sortOrder": "DESC",
                           "country": "", "port": "", "type": "http", "anonymity": "undefined",
                           "ping": "undefined",
                           "gproxy": "2"}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Host': 'hidester.com',
                'Referer': 'https://hidester.com/proxylist/'}

            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
                results = response.json()
                results = [x for x in results if x['type'] == 'http']
        except Exception as e:
            raise e
        return results

    def proxy_parser(self, data):
        results = []
        try:
            for result in data:
                result['address']=result['IP']
                result['port'] = result['PORT']
                results.append(result)
        except Exception as e:
            raise e
        return results



    def main(self):
        html_dict = self.get_data()
        checker = self.proxy_parser(html_dict)
        self.logger.log('get {} proxies'.format(len(checker)))
        proxies = proxy_checker(checker)
        save_proxy(proxies, type='http')

