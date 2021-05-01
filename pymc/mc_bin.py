# _*_ coding: utf-8 _*_
# @Time : 2021/3/29 上午 09:21 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : mc.py
# @Software : PyCharm
from .mc_enum import EnumSubTitle, EnumCmd
from .mc_device import MelsecElement
import math

m_nNetNo = 0x00
# PLC编号
m_nPLCNo = 0xFF
# IO编号
m_nIONo = 0xFF03
# 站编号
m_nStationNo = 0x00
# CPU监视定时器，命令输出到接收应答文件时间
m_nTimeOut = 0x1000
# # 命令
# self.m_cmd = cmd.value
# # 子命令
# self.m_sub_cmd = sub_cmd.value
# # 软元件
# self.m_MelsecElement = m_melsec_element
# # 起始软元件地址
# self.m_nElementStartAddr = element_start_addr
# # 软元件数据长度
# self.m_nElementDataLen = element_data_len
# # 软元件数据
# self.m_nElementData = element_data
# # 结束代码
# self.m_end_code = end_code.value
# # 临时存放字节数组
# self.m_byte_list = []
# 数据长度 不包括软元件数据
m_nDataLen = 12


def check(melsec_element: MelsecElement, start_addr, data_len) -> bool:
    """
    检查起始地址和读取长度
    """
    if data_len < 0 or data_len > melsec_element.m_nLen:
        return False
    if start_addr < melsec_element.m_nStartAddr or \
            start_addr > melsec_element.m_nEndAddr:
        return False
    return True


'''*************读协议内容******************************
*副标题(2)50 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|请求数据长度(2)_12
*应答超时(2)1000|命令(2)_|子命令(2)_|起始地址(3)_
*请求软元件代码(1)|请求点数长度(2)
****************************************************'''


def get_read_bytes(melsec_element: MelsecElement, start_addr, data_len) -> bytes:
    """
    读数据 MC 3E帧协议
    :param melsec_element: 软元件类型
    :param start_addr: 起始地址
    :param data_len: 读取数据长度
    :return: bytes
    """
    m_bytes = bytes()
    if check(melsec_element, start_addr, data_len):
        sub_title = EnumSubTitle.Request.value
        m_cmd = EnumCmd.ReadBatch.value
        m_bytes += int.to_bytes(sub_title, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nNetNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nPLCNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nIONo, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nStationNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nDataLen, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nTimeOut, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nSub_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(start_addr, 3, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nBinCode, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(data_len, 2, byteorder='little', signed=False)
    else:
        raise Exception('device addr or data length is error!')
    return bytes(m_bytes)


def get_read_bytes_4e(number, melsec_element: MelsecElement, start_addr, data_len) -> bytes:
    """
    读数据 MC 4E帧协议
    :param number: 序列号
    :param melsec_element: 软元件类型
    :param start_addr: 起始地址
    :param data_len: 读取数据长度
    :return: bytes
    """
    m_bytes = bytes()
    if check(melsec_element, start_addr, data_len):
        sub_title = EnumSubTitle.Request4e.value
        m_cmd = EnumCmd.ReadBatch.value
        m_bytes += int.to_bytes(sub_title, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(number, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(0, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nNetNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nPLCNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nIONo, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nStationNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nDataLen, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nTimeOut, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nSub_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(start_addr, 3, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nBinCode, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(data_len, 2, byteorder='little', signed=False)
    else:
        raise Exception('device addr or data length is error!')
    return bytes(m_bytes)


'''*************写协议内容******************************
*副标题(2)50 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|请求数据长度(2)_12+写入数据长度
*应答超时(2)1000|命令(2)_|子命令(2)_|起始地址(3)_
*请求软元件代码(1)|请求点数长度(2)|写入数据(分按位和按字)
****************************************************'''


def get_write_bytes(melsec_element: MelsecElement, start_addr, data) -> bytes:
    """
    写数据 MC 3E帧协议
    :param melsec_element: 软元件类型
    :param start_addr: 起始地址
    :param data: 数据内容list|int
    :return: bytes
    """
    m_bytes = bytes()
    if isinstance(data, int):
        data = [data, ]
    if check(melsec_element, start_addr, len(data)):
        sub_title = EnumSubTitle.Request.value
        m_cmd = EnumCmd.WriteBatch.value
        m_bytes += int.to_bytes(sub_title, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nNetNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nPLCNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nIONo, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nStationNo, 1, byteorder='little', signed=False)
        if melsec_element.m_nSub_cmd:
            data_len = math.ceil(len(data)/2)
        else:
            data_len = len(data) * 2
        total_data_len = m_nDataLen + data_len
        m_bytes += int.to_bytes(total_data_len, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nTimeOut, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nSub_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(start_addr, 3, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nBinCode, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(data_len, 2, byteorder='little', signed=False)

        if melsec_element.m_nSub_cmd:
            for i in range(0, len(data), 2):
                if i + 1 < len(data):
                    m_bytes += int.to_bytes(data[i] << 4 | data[i + 1], 1, byteorder='little', signed=False)
                else:
                    m_bytes += int.to_bytes(data[i] << 4, 1, byteorder='little', signed=False)
        else:
            for dt in data:
                m_bytes += int.to_bytes(dt, 2, byteorder='little', signed=False)

    return m_bytes


'''*************写协议内容******************************
*副标题(2)54 00|序列号(2)34 12|固定值(2)00 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|请求数据长度(2)_12+写入数据长度
*应答超时(2)1000|命令(2)_|子命令(2)_|起始地址(3)_
*请求软元件代码(1)|请求点数长度(2)|写入数据(分按位和按字)
****************************************************'''


def get_write_bytes_4e(number, melsec_element: MelsecElement, start_addr, data) -> bytes:
    """
    写数据 MC 4E帧协议
    :param number: 序列号
    :param melsec_element: 软元件类型
    :param start_addr: 起始地址
    :param data: 数据内容list|int
    :return: bytes
    """
    m_bytes = bytes()
    if isinstance(data, int):
        data = [data, ]
    if check(melsec_element, start_addr, len(data)):
        sub_title = EnumSubTitle.Request4e.value
        m_cmd = EnumCmd.WriteBatch.value
        m_bytes += int.to_bytes(sub_title, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(number, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(0, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nNetNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nPLCNo, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nIONo, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_nStationNo, 1, byteorder='little', signed=False)
        if melsec_element.m_nSub_cmd:
            data_len = math.ceil(len(data) / 2)
        else:
            data_len = len(data) * 2
        total_data_len = m_nDataLen + data_len
        m_bytes += int.to_bytes(total_data_len, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(m_nTimeOut, 2, byteorder='big', signed=False)
        m_bytes += int.to_bytes(m_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nSub_cmd, 2, byteorder='little', signed=False)
        m_bytes += int.to_bytes(start_addr, 3, byteorder='little', signed=False)
        m_bytes += int.to_bytes(melsec_element.m_nBinCode, 1, byteorder='little', signed=False)
        m_bytes += int.to_bytes(len(data), 2, byteorder='little', signed=False)

        if melsec_element.m_nSub_cmd:
            for i in range(0, len(data), 2):
                if i+1 < len(data):
                    m_bytes += int.to_bytes(data[i] << 4 | data[i+1], 1, byteorder='little', signed=False)
                else:
                    m_bytes += int.to_bytes(data[i] << 4, 1, byteorder='little', signed=False)
        else:
            for dt in data:
                m_bytes += int.to_bytes(dt, 2, byteorder='little', signed=False)
    return m_bytes

# MCBinSend: 500000FFFF03000E001000011400000000009D0100000F 按字写
# MCBinRece: D00000FFFF030002000000

'''*************读应答正常协议内容******************************
*副标题(2)D0 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|应答数据长度(2)_
*结束代码(2)00 00|应答数据部分
**********************************************************'''


def get_read_respond(byte_respond: bytes):
    data_len = 0
    if len(byte_respond) > 11:
        data_len = int.from_bytes(byte_respond[7:9], byteorder='little', signed=False) - 2
    if data_len >= len(byte_respond) - 11:
        return byte_respond[11:11+data_len]
    else:
        return None

'''*************读应答正常协议内容******************************
*副标题(2)D4 00|序列号(2)34 12|固定值(2)00 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|应答数据长度(2)_
*结束代码(2)00 00|应答数据部分
**********************************************************'''


def get_read_respond_4e(byte_respond: bytes):
    data_len = 0
    if len(byte_respond) > 15:
        data_len = int.from_bytes(byte_respond[11:13], byteorder='little', signed=False) - 2
    if data_len >= len(byte_respond) - 15:
        number = int.from_bytes(byte_respond[2:4], byteorder='little', signed=False)
        return number, byte_respond[15:15+data_len], data_len+15
    else:
        return None

'''*************写应答正常协议内容******************************
*副标题(2)D0 00|网络编号(1)00|PLC编号(1)FF
*IO编号(2)FF 03|站编号(1)00|应答数据长度(2)02 00
*结束代码(2)00 00
*D0 00 |00 |FF |FF 03| 00| 02 00 |00 00
**********************************************************'''


def get_write_respond(byte_respond: bytes):
    """
    MC 3E帧回复
    :param byte_respond:
    :return:
    """
    str_respond = ''.join(["%02X" % b for b in byte_respond])
    str_temp = "D00000FFFF030002000000"
    return str_respond == str_temp

'''*************写应答正常协议内容******************************
*副标题(2)D4 00|序列号(2)34 12|固定值(2)00 00|网络编号(1)00
*PLC编号(1)FF|IO编号(2)FF 03|站编号(1)00|应答数据长度(2)02 00
*结束代码(2)00 00
*D0 00 |00 |FF |FF 03| 00| 02 00 |00 00
**********************************************************'''


def get_write_respond_4e(byte_respond: bytes):
    """
    MC 4E帧写回复
    :param byte_respond:
    :return number,result,index:
    """
    number = int.from_bytes(byte_respond[2:4], byteorder='little', signed=False)
    respond = byte_respond[:2] + byte_respond[6:15]
    str_respond = ''.join(["%02X" % b for b in respond])
    # print(str_respond)
    str_temp = "D40000FFFF030002000000"
    return number, str_respond == str_temp, 15


'''*************应答异常协议内容******************************
 *副标题(2)D0 00|网络编号(1)00|PLC编号(1)FF
 *IO编号(2)FF 03|站编号(1)00|应答数据长度(2) 0B 00
 *结束代码(2)51 C0
 *网络编号(1)00|PLC编号(1)FF
 *IO编号(2)FF 03|站编号(1)00|命令(2)|子命令(2)
********************************************************'''


def get_respond_code(byte_respond: bytes):
    if len(byte_respond) > 10:
        return int.from_bytes(byte_respond[9:11], byteorder='little', signed=False)
    return -1


'''*************应答异常协议内容******************************
 *副标题(2)D4 00|序列号(2)34 12|固定值(2)00 00|网络编号(1)00|PLC编号(1)FF
 *IO编号(2)FF 03|站编号(1)00|应答数据长度(2) 0B 00
 *结束代码(2)51 C0
 *网络编号(1)00|PLC编号(1)FF
 *IO编号(2)FF 03|站编号(1)00|命令(2)|子命令(2)
********************************************************'''


def get_respond_code_4e(byte_respond):
    if len(byte_respond) > 14:
        number = int.from_bytes(byte_respond[2:4], byteorder='little', signed=False)
        return number, int.from_bytes(byte_respond[13:15], byteorder='little', signed=False), 24

    return 0, -1


