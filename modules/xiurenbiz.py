import re
import os
import requests
from bs4 import BeautifulSoup

import Utils

def download(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')  # 转编码
    content_inner = soup.findAll('div', class_="content-inner")[0].find("p")
    #for i in content_inner:
    #    print(i)
    z = 0
    for i in content_inner.find_all('img'):
        src = i["src"]
        img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', src)[0]  # 后缀
        #print(i["title"] + " " + str(z) + img_format)
        if i != 0:
            Utils.download(str(z) + img_format, src, i["title"] + os.sep)
        z = z + 1
