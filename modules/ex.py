import os
import re
import threading
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

SizeOrDownloads = 1  # 获取种子模式:0则为选择文件大小 1则为选择下载次数
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}
cookie = {'ipb_member_id': '49635', 'ipb_pass_hash': '22b275993d8d3bdb4bca2aeef050210e', 'igneous': '75267c0b7',
          'sk': 'uhshzwzisiq0rjb6rmzxirgtvv7v'}
Directory = 'torrent'
isProxy = 0  # 是否开启代理
thread_max_num = threading.Semaphore(3)  # 同时进行的线程数,默认定义为2
s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))
path = ''
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

    # 开启BT客户端进行下载
    def executeBTClient(self):
        s = 'explorer \"' + self + '\"'
        os.system(s)

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

    # 下载并执行BT种子
    def download_torrent(self, title):
        print('正在下载种子')
        path = Utils.filePath + os.sep + Directory + os.sep
        if not os.path.exists(path):
            os.mkdir(path)

        response = Utils.getRequest(self)
        torrentPath = path + title + r'.torrent'
        with open(torrentPath, 'wb') as g:
            g.write(response.content)
        Utils.executeBTClient(torrentPath)  # 执行打开BT种子

    # 获取所需要下载的种子链接,需要传入种子页面地址,返回种子地址
    def getTorrentUrl(self):
        bookTorrentTitle = []
        bookTorrentUrl = []
        r = Utils.getRequest(self)
        soup = BeautifulSoup(r.text, 'html.parser')
        # 开始获取种子大小(所想要下载的文件SIZE:417.05MB)
        myMaximum = 0.00
        count = 0
        tmpCount = 0
        for k in soup.find_all('td'):
            if SizeOrDownloads == 0:
                if re.search('Size:', k.text):
                    myNowTorrnet = getSODString(k)
                    # 若种子文件小于或等于获取文件则等于获取的种子
                    if myMaximum <= myNowTorrnet:
                        myMaximum = myNowTorrnet
                        count = tmpCount
                    tmpCount += 1
            else:
                if re.search('Downloads', k.text):
                    myNowTorrnet = getSODString(k)
                    # 若种子文件小于或等于获取文件则等于获取的种子
                    if myMaximum <= myNowTorrnet:
                        myMaximum = myNowTorrnet
                        count = tmpCount
                    tmpCount += 1
        for k in soup.find_all('a'):
            if re.search('http', k['href']):
                bookTorrentTitle.append(k.string)
                bookTorrentUrl.append(k['href'])  # 获取到的下载地址
        Utils.download_torrent(bookTorrentUrl[count], bookTorrentTitle[count])

    # 获取页面的Torrent download()地址
    def DownloadStart(self):
        r = Utils.getRequest(self)
        soup = BeautifulSoup(r.text, 'html.parser')
        for k in soup.find_all('a', href='#'):
            # if re.search('''onclick="return popUp\(\'''', str(k)):
            # 可获取Archive Download Torrent Download
            # 只获取Torrent Download
            if re.search('gallerytorrents', str(k)):
                # 若果没有种子，则执行抓图
                if re.search('0', str(k.string)):
                    title = ''  # 获取标题
                    try:
                        gj = soup.find(id='gj').string  # 先获取日文标题，若没有则获取普通标题
                        if gj is None:
                            title = soup.find(id='gn').string
                        else:
                            title = gj
                    except:
                        title = soup.find(id='gn').string
                    pageCount = Utils.getPageCount(soup)  # 获取有多少页面
                    count = 1
                    title = title.replace('/', ' ')
                    path = Utils.filePath + os.sep + title + os.sep
                    # 若果只有一页
                    if pageCount == 0:
                        # 先获取页面
                        pictureCollection = []
                        for page1gdtm in soup.find_all('div', class_='gdtm'):
                            page1gdtma = page1gdtm.find('a')
                            pictureCollection.append(page1gdtma['href'])
                            print(page1gdtma['href'])
                        # 循环下载
                        for link in pictureCollection:
                            # 若存在将要下载的文件，则跳过下载
                            if os.path.exists(path + str(count) + '.jpg'):
                                pass
                            else:
                                Utils.PictureDownload(link, str(count), title)
                                count += 1
                    else:
                        # 多页面，先缓存页面，再进行处理
                        pictureCollection = []
                        for page1gdtm in soup.find_all('div', class_='gdtm'):
                            page1gdtma = page1gdtm.find('a')
                            pictureCollection.append(page1gdtma['href'])
                            print(page1gdtma['href'])
                        for num in range(1, pageCount + 1):
                            htmllink = self + '?p=' + str(num)  # 页面地址
                            Utils.getPAGECAHCE(htmllink, filename=str(num), title=title)  # 下载页面缓存
                            path = Utils.filePath + os.sep + 'cache' + os.sep + title + os.sep + str(num) + '.txt'  # 路径名
                            htmlfile = open(path, 'r', encoding='utf-8')  # 读取html文件
                            htmlr = htmlfile.read()  # 读取html
                            gdtmsoup = BeautifulSoup(htmlr, 'html.parser')  # html过滤
                            for gdtm in gdtmsoup.find_all('div', class_='gdtm'):
                                a = gdtm.find('a')
                                pictureCollection.append(a['href'])
                                print(a['href'])
                        # 循环下载
                        for link in pictureCollection:
                            if os.path.exists(path + str(count) + '.jpg'):
                                pass
                            else:
                                Utils.PictureDownload(link, str(count), title)
                                count += 1
                else:
                    # 查找到有种子，进行下载种子
                    torrentURL = k.attrs['onclick']
                    pattern = re.compile(
                        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                    url = re.findall(pattern, torrentURL)
                    # 获取到的Torrent Download连接
                    Utils.getTorrentUrl(url[0].split('\'')[0])

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
    def DirectPictureDownload(self, type_dl, checkResult, x_path):
        Utils.filePath = x_path
        # gdtl 为 EX图片页面   gdtm为e-hentai页面
        if checkResult == 0:
            page_div_class = "gdtl"
        elif checkResult == 1:
            page_div_class = "gdtm"
            perPageCount = 40

        r = Utils.getRequest(self)
        soup = BeautifulSoup(r.text, 'html.parser')
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
            for page1gdtm in soup.find_all('div', class_=page_div_class):
                page1gdtma = page1gdtm.find('a')['href']
                pictureCollection.append(page1gdtma)
                print("page1gdtma:{}".format(page1gdtma))
        else:
            # 多页面，先缓存页面，再进行处理
            for page1gdtm in soup.find_all('div', class_=page_div_class):
                page1gdtma = page1gdtm.find('a')['href']
                pictureCollection.append(page1gdtma)
                print("page1gdtma(2):{}".format(page1gdtma))
            for num in range(1, pageCount + 1):
                r = Utils.getRequest(self + '?p=' + str(num))
                gdtmsoup = BeautifulSoup(r.text, 'html.parser')  # html过滤
                for gdtm in gdtmsoup.find_all('div', class_=page_div_class):
                    a = gdtm.find('a')['href']
                    pictureCollection.append(a)
                    print("a:{}".format(a))
                time.sleep(1)  # 防止抓页面数量太快被封

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
