import sys

import Utils

argvalue = sys.argv[1:]


# 主方法
def main():
    if len(argvalue) != 0:
        print(argvalue)
        Utils.checkURL(argvalue[0])


if __name__ == '__main__':
    main()
