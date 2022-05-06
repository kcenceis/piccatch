import os
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

import Utils


def download(url):
    Page_result = Utils.getRequest(url)
    soup = BeautifulSoup(Page_result.text, 'html.parser')
    pic_name = Utils.getUrlParams(url, 'id')
    # 获取TAG 用于 文件名
    ul_tag_sidebar = soup.find_all('ul', id='tag-sidebar')
    for i in ul_tag_sidebar:
        artist = i.find_all('li', class_="tag-type-artist")
        character = i.find_all('li', class_="tag-type-character")
        copyright = i.find_all('li', class_="tag-type-copyright")
        pic_name = Utils.catchname(pic_name, artist)
        pic_name = Utils.catchname(pic_name, character)
        pic_name = Utils.catchname(pic_name, copyright)
    print(pic_name)

    # 获取图片链接 和 后缀
    div_class_link_list = soup.find_all('div', class_='link-list')
    for i in div_class_link_list:
        for x in i.find_all('li'):
            bz = '''Original image'''
            if re.search(bz, str(x)):
                pic_url = x.a['href']  # 图片链接
                print("图片的链接:" + pic_url)
                # 开始获取图片后缀
                file_ = os.path.basename(urlparse(pic_url).path)
                print("原图片名:" + file_)
                img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', file_)[0]  # 后缀
    Utils.download(pic_name + img_format, pic_url)
