#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""get the ip location of google homepage
"""

__author__ = 'LGX95'
__date__ = '2020-03'

import re
from urllib import request


url = 'https://www.google.com/search?q=what+is+my+ip&oq=what+is+my+ip&aqs=chrome..69i57j69i61.7202j0j1&sourceid=chrome&ie=UTF-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}


def get(url, headers):
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    return resp.read().decode('utf-8')


def write_tmp(html):
    with open('google.html', 'w') as f:
        f.write(html)


def extract_location(html):
    """just use re to extract location
    """
    re_pmc = re.findall(r"pmc='(.*?)'", html)
    matched = re.findall(r'\\x22uul_text\\x22:\\x22(.*?)\\x22', re_pmc[0])
    return matched


if __name__ == '__main__':
    resp = get(url, headers)
    write_tmp(resp)
    location = extract_location(resp)
    print(location)
