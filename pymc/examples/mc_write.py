# _*_ coding: utf-8 _*_
# @Time : 2021/4/28 上午 11:36 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : demo_mnetg.py
# @Software : PyCharm
import sys
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

from pymc import *


def main():
    worker = McWorker("192.168.3.39", 8000)
    worker.connect()
    if worker.is_connected():
        print("Mc Connect Success!")

    while True:
        input_str = input('请输入寄存器地址(W0000,10|B0000,10):')
        length = 1
        if len(input_str.split(',')) == 2:
            length = input_str.split(',')[1]
            input_str = input_str.split(',')[0]
        try:
            print(worker.write(input_str, int(length)))
        except Exception as e:
            # print("输入错误, 程序终止",e)
            # mc.close_connect()
            # break
            print(e)


if __name__ == '__main__':
    main()
