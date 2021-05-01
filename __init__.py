# _*_ coding: utf-8 _*_
# @Time : 2021/4/9 下午 02:31 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : __init__.py
# @Software : PyCharm
from .mc_read_write_4e import Mc
from .mc_device import DeviceType as dt
from .base_worker import BaseWorker
import time


class McWorker(BaseWorker):
    """
    MC协议4E帧 工作类
    """
    def __init__(self, ip, port):
        self.mc = Mc(ip, port)

    def connect(self):
        self.mc.keep_connect()
        count = 0
        while self.is_connected():
            time.sleep(0.5)
            count += 1
            if count > 10:
                self.disconnect()
                return False
        return True

    def disconnect(self):
        self.mc.close_connect()

    def is_connected(self):
        return self.mc.is_connected()

    def _get_device_type(self, device):
        start_addr = int(device[len(device) - 4:], 16)
        device_type = device[:len(device)-4]
        if hasattr(dt, device_type):
            device_type = getattr(dt, device_type)
        else:
            raise Exception(f"device_type({device_type}) is error")
        return device_type, start_addr

    def read(self, device, length):
        """
        读数据
        :param device: 软元件(D0000)
        :param length: 读取长度
        :return: dic
        """
        device_type, start_addr = self._get_device_type(device)
        return self.mc.read(device_type, start_addr, length)

    def write(self, device, data):
        """
        写数据
        :param device: 软元件(D0000)
        :param data: list
        :return: dic
        """
        device_type, start_addr = self._get_device_type(device)
        return self.mc.write(device_type, start_addr, data)

