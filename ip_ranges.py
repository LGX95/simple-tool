#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This scripts use to get google cloud ip ranges
Ref: https://cloud.google.com/compute/docs/faq#find_ip_range
"""

__author__ = 'lgx'
__date__ = '2020-10'

import ipaddress
import subprocess as sp
from typing import List

import httpx

gcp_dns_url = '_cloud-netblocks.googleusercontent.com'


def run_dig(name: str, server: str = '8.8.8.8', type_: str = 'TXT') -> str:
    """call dig
    """
    cmd = f'dig @{server} {name} {type_} +short'
    res = sp.check_output(cmd, stderr=sp.STDOUT, shell=True)
    return res.decode('utf8')


def get_gcp_ip_range_by_dig(dns_url: str,
                            ip_range_list: List[str]) -> List[str]:
    """get google cloud ip ranges by using dig
    """
    answer = run_dig(dns_url)
    # gcp_dns_url answer eg:
    #    "v=spf1 include:_cloud-netblocks1.googleusercontent.com
    #     include:_cloud-netblocks2.googleusercontent.com
    #     include:_cloud-netblocks3.googleusercontent.com
    #     include:_cloud-netblocks4.googleusercontent.com
    #     include:_cloud-netblocks5.googleusercontent.com ?all"
    for i in answer.split():
        if i.startswith('include'):
            # eg: include:_cloud-netblocks2.googleusercontent.com
            url = i.split(':')[1]
            get_gcp_ip_range_by_dig(url, ip_range_list)
        elif i.startswith('ip4'):
            # eg: ip4:34.100.0.0/16
            ip_range = i.split(':')[1]
            ip_range_list.append(ip_range)
    return ip_range_list


def get_gcp_ip_ranges() -> List[str]:
    """get google cloud JSON-formatted list ip ranges
    """
    url = 'https://www.gstatic.com/ipranges/cloud.json'
    r = httpx.get(url)
    # r.josn() eg:
    #     {
    #         syncToken: "1602090128090",
    #         creationTime: "2020-10-07T10:02:08.09",
    #         prefixes: [
    #             {
    #                 ipv4Prefix: "34.80.0.0/15",
    #                 service: "Google Cloud",
    #                 scope: "asia-east1"
    #             }, ...]
    #     }
    ip_ranges = [
        i['ipv4Prefix'] for i in r.json()['prefixes'] if i.get('ipv4Prefix')
    ]
    return ip_ranges


def get_aws_ip_ranges() -> List[str]:
    """get aws json-formatted list ip ranges
    """
    url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    r = httpx.get(url)
    # r.json() eg:
    #     syncToken: "1602124876",
    #     createDate: "2020-10-08-02-41-16",
    #     prefixes: [
    #         {
    #             ip_prefix: "3.5.140.0/22",
    #             region: "ap-northeast-2",
    #             service: "AMAZON",
    #             network_border_group: "ap-northeast-2"
    #         }, ...
    #     ]
    #     ipv6_prefixes: [
    #         {
    #             ipv6_prefix: "2600:1f15::/32",
    #             region: "us-gov-east-1",
    #             service: "AMAZON",
    #             network_border_group: "us-gov-east-1"
    #         }, ...
    #     ]
    ip_ranges = [i['ip_prefix'] for i in r.json()['prefixes']]
    return ip_ranges


def collapse_ip_ranges(ip_range_list: List[str]) -> List[str]:
    """collapse ip ranges list
    """
    ips = [ipaddress.ip_network(ip) for ip in ip_range_list]
    cidrs = ipaddress.collapse_addresses(ips)
    return sorted([i.with_prefixlen for i in cidrs])


if __name__ == '__main__':
    gcp_ip_ranges = get_gcp_ip_ranges()
    gcp_cidrs = collapse_ip_ranges(gcp_ip_ranges)
    print(gcp_cidrs)

    aws_ip_ranges = get_aws_ip_ranges()
    aws_cidrs = collapse_ip_ranges(aws_ip_ranges)
    print(aws_cidrs)
