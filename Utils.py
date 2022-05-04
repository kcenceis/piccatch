from urllib import parse

import requests
from requests.adapters import HTTPAdapter

proxyON = True
# socks代理规则
proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'}

mReq = requests.session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/85.0.4183.83 Safari/537.36"}
mReq.mount('https://', HTTPAdapter(max_retries=3))
mReq.mount('http://', HTTPAdapter(max_retries=3))

# URL,需要获取的get参数
# 返回内容
def getUrlParams(url, params):
    return str(parse.parse_qs(url)[params][0])


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    return r
