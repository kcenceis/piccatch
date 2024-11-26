import os
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

import Utils


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    new_title = re.sub("\n", "", new_title)
    return new_title

def download(url):
    Page_result = Utils.getRequest(url)
    soup = BeautifulSoup(Page_result.text, 'html.parser')
    title = soup.find('h1', class_="post__title").text
    title = validateTitle(title)

    count = 0
    # 获取TAG 用于 文件名
    div_post = soup.find_all("div", class_=r"post__thumbnail")
    for i in div_post:
        a = i.find("a")["href"]
        count += 1
        file_ = os.path.basename(urlparse(a).path)
        img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', file_)[0]
        pic_name = str(count) + img_format
        Utils.download(pic_name, a, title + os.sep)
