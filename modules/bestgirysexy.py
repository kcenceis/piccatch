import re
import os
import Utils

from DrissionPage import ChromiumPage, ChromiumOptions

def download(url):
    co = ChromiumOptions()
    co.set_load_mode('eager') # 加载html后停止
    co.no_js(True) #不加载js
    co.no_imgs(True) # 不加载图片
    co.incognito()  # 无痕模式
    co.headless()  # 无头模式
    co.set_argument('--no-sandbox')
    co.set_argument('--window-size', '800,600')
    co.set_argument('--start-maximized')
    co.set_argument('--guest')
    co.set_argument("--disable-gpu")
    # 设置UA 防止被chromedriver自动添加headless标记 导致被检测到是机器人
    co.set_user_agent(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
    # 以该配置创建页面对象
    page = ChromiumPage(co)
    # try防止报错后，程序不中止
    try:
        # 进行请求
        page.get(url)
        title = page.ele('tag:title').inner_html
        # 从0开始命名图片名字
        z = 0
        # 开始抓取
        for i in page.eles('tag:img@class=aligncenter size-full'):
            # 获取图片链接
            src = i.attr('src')
            # 获取后缀名
            z = z + 1
            img_format = re.findall('(.jpg|.bmp|.png|.jpeg|.webp|.gif|.mp4|.rar|.zip)', src)[0]
            print(os.path.split(os.path.realpath(__file__))[0]+os.sep+str(title) + os.sep)
            # 进行下载
            page.download(file_url=src,save_path=Utils.filePath+str(title) + os.sep,rename=str(z)+img_format,file_exists="skip",timeout=20)
    finally:
        # 关闭页面
        page.quit()
