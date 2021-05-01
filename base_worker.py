# _*_ coding: utf-8 _*_
# @Time : 2021/4/28 上午 11:16 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : base_worker.py
# @Software : PyCharm


class BaseWorker:

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def is_connected(self):
        raise NotImplementedError

    def read(self, device, length):
        """
        读数据
        :param device: 软元件(D0000)
        :param length: 读取长度
        :return: dic
        """
        raise NotImplementedError

    def write(self, device, data):
        """
        写数据
        :param device: 软元件(D0000)
        :param data: list
        :return: dic
        """
        raise NotImplementedError