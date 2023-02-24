import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import Utils


def download(url):
    domain = "https://" + '.'.join(url.split('/')[2].split('.')) + "/"
    Page_result = Utils.getRequest(url)
    soup = BeautifulSoup(Page_result.text.encode('latin1').decode('utf-8'), 'html.parser')  # 转编码
    # 标题 用于命名文件夹
    title = soup.find('div', class_='item_title').find('h1').text
    # 一页有4个content  0 页数 1 图片 2 页数 3 推荐页面
    content = soup.find_all('div', class_="content")
    # 获取 页数
    content_left = content[0].find_all('div', class_="content_left")
    page = content_left[0].find_all('div', class_='page')
    a = page[0].find_all('a')

    htmlpage_list = []  # 页面的地址
    src_list = []  # 图片的下载链接

    for i in a:
        stri = str(i)
        if re.search('href=', stri):
            if re.search("下页", stri):
                continue
            else:
                htmlpage_list.append(domain + i['href'])

    for i in htmlpage_list:
        New_Page_result = Utils.getRequest(i)
        New_soup = BeautifulSoup(New_Page_result.text.encode('latin1').decode('utf-8'), 'html.parser')  # 转编码
        New_content = New_soup.find_all('div', class_="content")
        for i in New_content[1].find_all('img'):
            src_list.append(domain + i['src'])

    # Utils.filePath = Utils.filePath + title + os.sep  # 获取脚本当前目录

    for i in range(len(src_list)):
        img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', src_list[i])[0]  # 后缀
        Utils.download(str(i + 1) + img_format, src_list[i], title + os.sep)
