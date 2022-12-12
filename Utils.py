import os
import re
from urllib import parse

import requests
from requests.adapters import HTTPAdapter

from modules import sankaku, rule34, gelbooru, xiurenb, ex

proxyON = False
# socks代理规则
proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'}

mReq = requests.session()
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/90.0.4430.93 Safari/537.36 "
headers['Content-Type'] = "application/x-www-form-urlencoded"
headers['dnt'] = "1"
headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
headers['sec-fetch-site'] = 'same-origin'
headers['sec-fetch-dest'] = 'document'
headers['upgrade-insecure-requests'] = '1'

mReq.mount('https://', HTTPAdapter(max_retries=3))
mReq.mount('http://', HTTPAdapter(max_retries=3))

filePath = os.path.split(os.path.realpath(__file__))[0] + os.sep  # 获取脚本当前目录
filePath = filePath + "Picture" + os.sep


def download(filename, url):
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    try:
        with open(filePath + filename, 'wb') as f:
            picBinary = getRequest(url)
            f.write(picBinary.content)
    except:
        pass


# URL,需要获取的get参数
# 返回内容
def getUrlParams(url, params):
    return str(parse.parse_qs(url)[params][0])


def catchname(pic_name, soup):
    if len(soup) < 4:
        for x in soup:
            pic_name += "_" + x.find('a').text
    else:
        for x in range(3):
            pic_name += "_" + soup[x].find('a').text
    return pic_name


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    return r


# 返回判断URL结果
def checkURL(message):
    # if re.search(r'https://exhentai.org/g/', message) or re.search(r'https://e-hentai.org/g/', message):
    if re.search(r'https://chan.sankakucomplex.', message):
        sankaku.download(message)
    elif re.search(r'https://rule34.', message):
        rule34.download(message)
    elif re.search(r'https://gelbooru.', message):
        gelbooru.download(message)
    elif re.search(r'https://www.xiurenb.', message):
        xiurenb.download(message)
    elif re.search(r'https://exhentai.org/g/', message):
        ex.Utils.DirectPictureDownload(message, False, 0, filePath)
    elif re.search(r'https://e-hentai.org/g/', message):
        ex.Utils.DirectPictureDownload(message, False, 1, filePath)

    else:
        print("退出程序")
        exit(0)
