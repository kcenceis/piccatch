import json
import os
import re
from urllib import parse

import requests
from requests.adapters import HTTPAdapter

from modules import sankaku, rule34, gelbooru, xiurenb, ex, kemono,xiurenbiz,bestgirysexy

#proxy_link = requests.get("http://127.0.0.1/proxy_link.json").text
#proxy_json = json.loads(proxy_link)
#proxyON = proxy_json["On"]
# socks代理规则
#proxies = {'http': proxy_json["proxy"],
 #          'https': proxy_json["proxy"]}
proxyON = 0
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
intab = r'[?*/\|.:><]'


def fixname(filename):
    filename = re.sub(intab, "", filename)
    return filename


def download(filename, url, new_file_path=""):
    print(url)
    download_path = filePath
    if new_file_path != "":
        download_path = filePath + new_file_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)
    else:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    try:
        with open(download_path + filename, 'wb') as f:
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
    if proxyON == 1:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, timeout=10)
    return r


# 返回判断URL结果
def checkURL(message):
    # if re.search(r'https://exhentai.org/g/', message) or re.search(r'https://e-hentai.org/g/', message):
    if re.search(r'https://chan.sankakucomplex.', message):
        sankaku.download(message)
    elif re.search(r'https://rule34.xxx', message):
        rule34.download(message)
    elif re.search(r'https://gelbooru.', message):
        gelbooru.download(message)
    elif re.search(r'https://www.xiuren51', message):
        xiurenb.download(message)
    elif re.search(r'https://exhentai.org/g/', message):
        ex.Utils.DirectPictureDownload(message, False, 0, filePath)
    elif re.search(r'https://e-hentai.org/g/', message):
        ex.Utils.DirectPictureDownload(message, False, 1, filePath)
    elif re.search(r'https://kemono.su/', message):
        kemono.download(message)
    elif re.search(r'https://xiuren.biz/', message):
        xiurenbiz.download(message)
    elif re.search(r'https://bestgirlsexy.com/', message):
        bestgirysexy.download(message)

    else:
        print("不符合")
        # exit(0)
        # continue
