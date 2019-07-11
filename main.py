#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from crawler.Hidester import Hidester
from crawler.Proxy_list import Proxy_list
from crawler.Spys import Spys
from argparse import ArgumentParser

hidester = Hidester()
proxy_list = Proxy_list()
spys = Spys()

if __name__ == '__main__':
    crawler = ['hidester', 'proxy-list', 'spys']
    parser = ArgumentParser()
    parser.add_argument('-c', '--crawler', choices=crawler, required=True, help='crawler running')
    parser.add_argument('-p', '--path', help='path file')
    args = parser.parse_args()
    crawler = args.crawler
    path = True if args.path else False

    if crawler == 'hidester':
        hidester.main(path=path)
    elif crawler == 'proxy-list':
        proxy_list.main(path=path)
    elif crawler == 'spys':
        spys.main(path=path)
