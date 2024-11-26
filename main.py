import sys
import os
import Utils

argvalue = sys.argv[1:]


# 主方法
def main():
    if len(argvalue) != 0:
        if argvalue[0] == "1":
            path = os.path.split(os.path.realpath(__file__))[0] + os.sep
            print(path)
            if os.path.getsize(path+'url.txt') != 0:
                with open(path+'url.txt') as f:
                    for l in f:
                        result = l.replace('\n', '')
                        print("开始抓取:{}".format(result))
                        Utils.checkURL(result)
                open(path+'url.txt', 'w+').write('')
        else:
            Utils.checkURL(argvalue[0])


if __name__ == '__main__':
    main()
