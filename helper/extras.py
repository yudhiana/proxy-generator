import os
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
from json import dump
from helper.logger import Logger

current_path = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(current_path, os.pardir))


logger = Logger(__name__)


def get_html(url, payloads=None, headers=''):
    result = None
    if payloads:
        try:
            response = requests.request(method='POST', url=url, data=payloads, headers=headers)
            if response.status_code == 200:
                result = response.text
        except Exception as e:
            raise e
    else:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.text
        except Exception as e:
            raise e
    return result


def parser(html, selector):
    try:
        elements = PyQuery(html)
        result = elements(selector)
    except Exception as e:
        raise e
    return result


def bs4_parser(html, selector):
    try:
        html = BeautifulSoup(html, 'lxml')
        result = html.select(selector)
    except:
        raise
    return result


def save_proxy(proxies=None, type='global'):
    if proxies:
        file_name = '{}/json-proxy/proxy_{}.json'.format(root, type)
        try:
            with open(file_name, 'w') as outfile:
                dump(proxies, outfile, indent=4)
        except Exception as e:
            raise e


def proxy_checker(proxys):
    result = []
    for proxy in proxys:
        proxies = {
            'http': '{}:{}'.format(proxy['address'], proxy['port']),
            'https': '{}:{}'.format(proxy['address'], proxy['port'])
        }
        try:
            response = requests.get(url='https://www.lazada.co.id/', proxies=proxies, timeout=10)
            if response.status_code == 200:
                logger.log('ready proxy: {}'.format(proxies))
                result.append(proxy)
        except :
            pass
    return result
