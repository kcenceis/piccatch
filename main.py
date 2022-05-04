import re
import sys
from modules import sankaku, rule34

argvalue = sys.argv[1:]


# 返回判断URL结果
def checkURL(message):
    # if re.search(r'https://exhentai.org/g/', message) or re.search(r'https://e-hentai.org/g/', message):
    if re.search(r'https://chan.sankakucomplex.com/', message):
        sankaku.download(message)
    elif re.search(r'https://rule34.xxx/', message):
        rule34.download(message)
    else:
        print("退出程序")
        exit(0)


# 主方法
def main():
    if len(argvalue) != 0:
        print(argvalue)
        checkURL(argvalue[0])


if __name__ == '__main__':
    main()
