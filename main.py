from window import myui, init
from sys import exit
from glob import glob
import argparse
from utils import removefile, endwithSlash

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dst", help="the directory in which you want to save the video", type=str, default="./video/")
parser.add_argument("-t", "--tmp", help="the directory of tempfile", type=str, default="./temp/")
args = parser.parse_args()



if __name__ == '__main__':
    # 运行程序
    app = init()
    program=myui(endwithSlash(args.tmp), endwithSlash(args.dst))
    program.show()
    sign=app.exec_()
    removefile(glob(endwithSlash(args.tmp) + "*.*"))
    exit(sign)