import sys
import os
import Utils

argvalue = sys.argv[1:]


# 主方法
def main():
    if len(argvalue) != 0:
        if argvalue[0] == "1":
            if os.path.getsize('url.txt') != 0:
                with open('url.txt') as f:
                    for l in f:
                        result = l.replace('\n', '')
                        print("开始抓取:{}".format(result))
                        Utils.checkURL(result)
                open('url.txt', 'w+').write('')
        else:
            Utils.checkURL(argvalue[0])


if __name__ == '__main__':
    main()
