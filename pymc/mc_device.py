# _*_ coding: utf-8 _*_
# @Time : 2021/3/29 上午 11:03 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : mc_melsec_element.py
# @Software : PyCharm
from enum import Enum
from .mc_enum import EnumSubCmd


class MelsecElement:
    def __init__(self, name: str, asc_code: str, bin_code: int, start_addr: int,
                 end_addr: int, sub_cmd: EnumSubCmd, n_len=3584):
        self.m_strName = name
        self.m_strAscCode = asc_code
        self.m_nBinCode = bin_code
        self.m_nStartAddr = start_addr
        self.m_nEndAddr = end_addr
        self.m_nSub_cmd = sub_cmd.value
        # 最大处理长度
        self.m_nLen = n_len

    def __str__(self):
        return self.m_strName + '/' + self.m_strAscCode


class DeviceType:
    """
    软元件类型
    """
    SM = MelsecElement("特殊继电器", "SM", 0x91, 0x000000, 0x002047, EnumSubCmd.Bit)
    SD = MelsecElement("特殊寄存器", "SD", 0xA9, 0x000000, 0x002047, EnumSubCmd.Word, 960)
    X = MelsecElement("输入继电器", "X*", 0x9C, 0x000000, 0x001FFF, EnumSubCmd.Bit)
    Y = MelsecElement("输出继电器", "Y*", 0x9D, 0x000000, 0x001FFF, EnumSubCmd.Bit, 7168)
    M = MelsecElement("内部继电器", "M*", 0x90, 0x000000, 0x008191, EnumSubCmd.Bit, 7904)
    L = MelsecElement("锁存继电器", "L*", 0x92, 0x000000, 0x008191, EnumSubCmd.Bit)
    F = MelsecElement("报警继电器", "F*", 0x93, 0x000000, 0x002047, EnumSubCmd.Bit)
    V = MelsecElement("边沿继电器", "V*", 0x94, 0x000000, 0x002047, EnumSubCmd.Bit)
    B = MelsecElement("链接继电器", "B*", 0xA0, 0x000000, 0x001FFF, EnumSubCmd.Bit)
    D = MelsecElement("数据寄存器", "D*", 0xA8, 0x000000, 0x012287, EnumSubCmd.Word, 960)
    W = MelsecElement("链接寄存器", "W*", 0xB4, 0x000000, 0x001FFFF, EnumSubCmd.Word, 960)
    TS = MelsecElement("定时器触点", "TS", 0xC1, 0x000000, 0x002047, EnumSubCmd.Bit)
    TN = MelsecElement("定时器线圈", "TN", 0xC0, 0x000000, 0x002047, EnumSubCmd.Bit)
    TC = MelsecElement("定时器当前值", "TC", 0xC2, 0x000000, 0x002047, EnumSubCmd.Word, 960)
    SS = MelsecElement("累计定时器触点", "SS", 0xC7, 0x000000, 0x002047, EnumSubCmd.Bit)
    SC = MelsecElement("累计定时器线圈", "SC", 0xC6, 0x000000, 0x002047, EnumSubCmd.Bit)
    SN = MelsecElement("累计定时器当前值", "SN", 0xC8, 0x000000, 0x002047, EnumSubCmd.Word)
    CS = MelsecElement("计数器触点", "CS", 0xC4, 0x000000, 0x001023, EnumSubCmd.Bit)
    CC = MelsecElement("计数器线圈", "CC", 0xC3, 0x000000, 0x001023, EnumSubCmd.Bit)
    CN = MelsecElement("计数器当前值", "CN", 0xC5, 0x000000, 0x001023, EnumSubCmd.Word, 960)
    SB = MelsecElement("链接特殊继电器", "SB", 0xA1, 0x000000, 0x0007FF, EnumSubCmd.Bit)
    SW = MelsecElement("链接特殊寄存器", "SW", 0xB5, 0x000000, 0x0007FF, EnumSubCmd.Word, 960)
    S = MelsecElement("步进继电器", "S*", 0x98, 0x000000, 0x008191, EnumSubCmd.Bit)
    DX = MelsecElement("直接输入继电器", "DX", 0xA2, 0x000000, 0x001FFF, EnumSubCmd.Bit)
    DY = MelsecElement("直接输出继电器", "DY", 0xA3, 0x000000, 0x001FFF, EnumSubCmd.Bit)
    SM = MelsecElement("特殊继电器", "SM", 0x91, 0x000000, 0x002047, EnumSubCmd.Bit)
    RZ = MelsecElement("文件寄存器Z", "RZ", 0xB0, 0x0FE7FF, 0x000015, EnumSubCmd.Word, 960)
    R = MelsecElement("文件寄存器", "R*", 0xAF, 0x032767, 0x000015, EnumSubCmd.Word, 960)
