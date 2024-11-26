import json
import os
import re
import threading
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

SizeOrDownloads = 1  # 获取种子模式:0则为选择文件大小 1则为选择下载次数
with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"config.json", "r") as f:
    result = json.loads(f.read())
    headers = {"User-Agent": result['User-Agent']}
    cookie = {'ipb_member_id': result['ipb_member_id'],
              'ipb_pass_hash': result['ipb_pass_hash'],
              'igneous': result['igneous'],
              'sk': result['sk']}
thread_max_num = threading.Semaphore(3)  # 同时进行的线程数,默认定义为2
s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))
perPageCount = 20


# 字符处理
def getSODString(self):
    [s.extract() for s in self('span')]
    myNowTorrnet = self.text.replace('MB', '').replace(' ', '')  # 种子大小
    myNowTorrnet = float(myNowTorrnet)  # myNowTorrnet转换为float
    return myNowTorrnet


# 将不能作为文件名的字符替换为下划线
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


# 线程操作
class MyThread(threading.Thread):
    def __init__(self, link, count, title):
        threading.Thread.__init__(self)
        self.link = link
        self.count = count
        self.title = title

    def run(self):
        with thread_max_num:
            Utils.PictureDownload(self.link, self.count, self.title)


class Utils:
    filePath = ''

    def getRequest(self):
        return s.get(url=self, cookies=cookie, headers=headers, timeout=5)

    # 下载图片
    def download_img(self, filename, title):
        path = Utils.filePath  + os.sep + validateTitle(title) + os.sep
        if not os.path.exists(path):
            os.makedirs(path)
        time.sleep(1)  # 防止抓页面数量太快被封
        r = Utils.getRequest(self)
        with open(path + validateTitle(filename) + r'.jpg', 'wb') as g:
            g.write(r.content)
        time.sleep(1)  # 防止抓页面数量太快被封

    # 获取图片下载连接,直接图片下载
    def PictureDownload(self, filename, title):
        r = Utils.getRequest(self)  # 请求网页
        soup = BeautifulSoup(r.text, 'html.parser')

        # 防止图片本身就没有原图 div_i7为原大小 div_i3为web中显示的图片(缩小版)
        k = soup.find('div', id='i7')
        if re.search('<a href="(.+?)">', str(k)):
            a_href = k.find('a')['href']
        # 没有获取到最大图 则直接使用web图
        else:
            k = soup.find('div', id='i3')
            a_href = k.find('img')['src']
        Utils.download_img(a_href, str(filename), str(title))

    # 返回到底有多少页需要获取,传入soup对象
    def getPageCount(self):
        # 若无gdt2则报错，直接返回页面只有1页
        for k in self.find_all('td', 'gdt2'):
            if re.search('pages', str(k)):
                pages = int(str(k.string).replace('pages', '').replace(' ', ''))
                # 40页图片一个页面 第一页无p=1,第二页为?p=1,第三页为?p=2,所以图片数/40的整数，等于所要运行取多次页面的次数，108/40=2，需要获取额外的两页
                pages = int(pages / perPageCount)
        return pages

    # 直接抓取页面的图片
    # 抓不到页面就是page_div_class改了，div的逻辑变了
    def DirectPictureDownload(self, type_dl, checkResult, x_path):
        Utils.filePath = x_path
        # gdtl 为 EX图片页面   gdtm为e-hentai页面
        if checkResult == 0:
            page_div_class = "gt200"
        elif checkResult == 1:
            page_div_class = "gt200"

        r = Utils.getRequest(self)
        soup = BeautifulSoup(r.text, 'html.parser')
        # 获取标题
        try:
            gj = soup.find(id='gj').string  # 先获取日文标题，若没有则获取普通标题
            if gj is None:
                title = soup.find(id='gn').string
            else:
                title = gj
        except:
            title = soup.find(id='gn').string

        title = title.replace('/', ' ')  # 防止文件夹带有/ 例如fate/go

        pageCount = Utils.getPageCount(soup)  # 获取有多少页面
        pictureCollection = []
        # 若果只有一页
        if pageCount == 0:
            # 先获取页面
            div_gt200 = soup.find('div', class_=page_div_class)
            for i in div_gt200.find_all('a'):
                pictureCollection.append(i['href'])
        else:
        # 若有多页
            # 抓取第一页
            div_gt200 = soup.find('div', class_=page_div_class)
            for i in div_gt200.find_all('a'):
                pictureCollection.append(i['href'])
            # 抓取后面的页数
            for num in range(1, pageCount + 1):
                r = Utils.getRequest(self + '?p=' + str(num))
                div_gt200 = BeautifulSoup(r.text, 'html.parser').find('div', class_=page_div_class)
                for i in div_gt200.find_all('a'):
                    pictureCollection.append(i['href'])
                time.sleep(1)

        path = Utils.filePath + os.sep + title + os.sep  # 定义下载目录
        # 循环下载
        for i in range(0, len(pictureCollection)):
            # 文件存在则不下载
            if os.path.exists(path + str(i + 1) + '.jpg'):
                pass
            else:
                # 单线程下载
                if not type_dl:
                    Utils.PictureDownload(pictureCollection[i], str(i + 1), title)
                else:
                    # 多线程下载
                    th = MyThread(pictureCollection[i], str(i + 1), title)
                    th.start()

#url,是否开启多线程，ex为0，x_path为下载目录
#Utils.DirectPictureDownload('https://exhentai.org/g/3135957/29161d2d15/',type_dl=False,checkResult=0,x_path="c:/asdasd/")

# def main():
#    if len(argvalue) != 0:
#        # 先判断地址是否是exhentai开头
#        checkResult = checkURL(argvalue[1])
#        if checkResult != 2:
#            # arg 0为单线程抓图 1为多线程抓图
#            if argvalue[0] == "0":
#                DirectPictureDownload(argvalue[1], type_dl=False, checkResult=checkResult)
#            if argvalue[0] == "1":
#                DirectPictureDownload(argvalue[1], type_dl=True, checkResult=checkResult)
