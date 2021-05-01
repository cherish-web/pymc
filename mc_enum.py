# _*_ coding: utf-8 _*_
# @Time : 2021/3/29 上午 08:57 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : cmd.py
# @Software : PyCharm
from enum import Enum


class EnumSubTitle(Enum):
    Request4e = 0x5400
    # 请求
    Request = 0x5000
    # 应答
    Respond = 0xD000
    Respond4e = 0xD400


class EnumEndCode(Enum):
    # 正常应答
    Ok = 0x0000
    # 异常应答
    Err = 0x51C0


class EnumCmd(Enum):
    # 成批读
    ReadBatch = 0x0401
    # 成批写
    WriteBatch = 0x1401


class EnumSubCmd(Enum):
    # 有存储扩展模块b7=0，b6=0：随机读出,监视数据注册用外
    # 按位读写
    Bit = 0x0001
    # 按字读写
    Word = 0x0000
    # 有存储扩展模块b7=1，b6=0：随机读出,监视数据注册用外
    # 按位读写
    BitEx = 0x0081
    # 按字读写
    WordEx = 0x0080


class EnumType(Enum):
    # 位类型
    Bit = 0
    # 字类型
    Word = 1





