#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""get the ip location of google homepage
"""

__author__ = 'LGX95'
__date__ = '2020-03'

import re
from urllib import request


url = 'https://www.google.com/?gws_rd=ssl'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
}
ignore_matched = [
    'YES',
    'News',
    'Shopping',
    'Books',
    'Account',
    'Search',
    'Maps',
    'YouTube',
    'Play',
    'Gmail',
    'Contacts',
    'Drive',
    'Calendar',
    'Translate',
    'Photos',
    'Duo',
    'Docs',
    'Sheets',
    'Slides',
    'Blogger',
    'Hangouts',
    'Keep',
    'Jamboard',
    'Collections']


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
    matched = re.findall(r'>([A-Za-z ]+)</span>', html)
    return [i for i in matched if i not in ignore_matched]


if __name__ == '__main__':
    resp = get(url, headers)
    write_tmp(resp)
    location = extract_location(resp)
    print(location)
