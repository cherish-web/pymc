# _*_ coding: utf-8 _*_
# @Time : 2021/4/1 上午 08:32 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : demo.py
# @Software : PyCharm
from mc_device import DeviceType as dt
from mc_read_write_4e import Mc
host = None
while True:
    ip_port = input('请输入PLC的IP及Port口(ip:port):')
    host = ip_port.split(':')
    if len(host) == 2:
        break
mc = Mc(host[0], int(host[1]))
mc.keep_connect()
while True:
    input_str = input('请输入寄存器地址(W/B):')
    length = 1
    if len(input_str.split(',')) == 2:
        length = input_str.split(',')[1]
        input_str = input_str.split(',')[0]
    device_type = input_str[:len(input_str)-4]
    try:
        start_addr = int(input_str[len(input_str)-4:], 16)
        if hasattr(dt, device_type):
            mc.write(getattr(dt, device_type), start_addr, [int(d) for d in length.split(':')])
    except Exception as e:
        # print("输入错误, 程序终止",e)
        # mc.close_connect()
        # break
        print(e)

