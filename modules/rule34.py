import os
from urllib import parse

from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

import Utils
from Utils import getRequest


def catchname(pic_name, soup):
    if len(soup) < 4:
        for x in soup:
            pic_name += "_" + x.find('a').text
    else:
        for x in range(3):
            pic_name += "_" + soup[x].find('a').text
    return pic_name


def download(url):
    # with open('3133.html', encoding="utf-8") as f:
    #    soup = BeautifulSoup(f.read(), 'html.parser')
    Page_result = getRequest(url)
    soup = BeautifulSoup(Page_result.text, 'html.parser')
    pic_name = Utils.getUrlParams(url, 'id')
    # 获取TAG 用于 文件名
    ul_tag_sidebar = soup.find_all('ul', id='tag-sidebar')
    for i in ul_tag_sidebar:
        artist = i.find_all('li', class_="tag-type-artist")
        character = i.find_all('li', class_="tag-type-character")
        copyright = i.find_all('li', class_="tag-type-copyright")
        pic_name = catchname(pic_name, artist)
        pic_name = catchname(pic_name, character)
        pic_name = catchname(pic_name, copyright)
    print(pic_name)

    # 获取图片链接 和 后缀
    div_class_link_list = soup.find_all('div', class_='link-list')
    # div_id_stats = soup.find_all('div', id='stats')
    # for i in div_id_stats:
    for i in div_class_link_list:
        for x in i.find_all('li'):
            bz = '''Original image'''
            if re.search(bz, str(x)):
                pic_url = x.a['href']  # 图片链接 并且补全url
                print("图片的链接:" + pic_url)
                # 开始获取图片后缀
                file_ = os.path.basename(urlparse(pic_url).path)
                print("原图片名:"+file_)
                img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', file_)[0]  # 后缀
    with open(pic_name + img_format, 'wb') as f:
        picBinary = getRequest(pic_url)
        f.write(picBinary.content)
