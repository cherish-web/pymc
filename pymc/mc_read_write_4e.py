# _*_ coding: utf-8 _*_
# @Time : 2021/3/31 上午 09:54 
# @Author : cherish_peng
# @Email : 1058386071@qq.com 
# @File : mc_read_write.py
# @Software : PyCharm
import asyncio
import time
from .mc_bin import *
from threading import Lock, Timer
from .mc_device import MelsecElement
from asyncio.protocols import Protocol
from asyncio.transports import Transport
from queue import SimpleQueue


class ClientProtocol(Protocol):
    def __init__(self, on_con_lost, callback_func):
        self.on_con_lost = on_con_lost
        self.connected = False
        self.response_data_queue_dic = {}
        self.response_data_mode_dic = {}
        self.transport = None
        self.response_data = bytes()
        self.lock1 = Lock()
        self.lock2 = Lock()
        self.change_connect_state = callback_func

    def check_data(self):
        if len(self.response_data) > 4:
            title = ''.join(["%02X" % b for b in self.response_data[:4]])
            if title != 'D400':
                with self.lock2:
                    self.response_data_queue_dic.clear()
                    self.response_data_mode_dic.clear()
                    self.response_data = bytes()
                return False
        return True

    def set_response_data_mode_que(self, num, que, is_read):
        with self.lock1:
            self.response_data_queue_dic[num] = que
            self.response_data_mode_dic[num] = is_read

    def rm_response_data_mode_que(self, num, index=0):
        with self.lock2:
            if num in self.response_data_queue_dic:
                del self.response_data_queue_dic[num]
            if num in self.response_data_mode_dic:
                del self.response_data_mode_dic[num]
            self.response_data = self.response_data[index:]

    def connection_made(self, transport: Transport) -> None:
        self.connected = True
        self.change_connect_state(self.connected)
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        print(''.join(["%02X" % b for b in data]))
        self.response_data += data
        if not self.check_data():
            return
        num, respond_code, index = get_respond_code_4e(self.response_data)
        if respond_code == -1:
            return
        elif respond_code > 0:
            res_que = self.response_data_queue_dic.get(num, None)
            is_read = self.response_data_mode_dic.get(num, None)
            if res_que is not None:
                res = {'res': None, 'code': respond_code, 'desc': f'mc {"read" if is_read else "write"} error'}
                res_que.put(res)
            self.rm_response_data_mode_que(num, index)
            return
        res_que = self.response_data_queue_dic.get(num, None)
        is_read = self.response_data_mode_dic.get(num, None)
        if is_read:
            num, res_data, index = get_read_respond_4e(self.response_data)
        else:
            num, res_data, index = get_write_respond_4e(self.response_data)
        if res_data is not None:
            self.rm_response_data_mode_que(num, index)
            if res_que is not None:
                return res_que.put({'res': res_data, 'code': respond_code, 'desc': ''})

    def connection_lost(self, exc):
        print('服务器连接断开')
        self.connected = False
        self.change_connect_state(self.connected)
        self.on_con_lost.set_result(True)


class Mc:
    def __init__(self, ip, port=1025):
        self.ip = ip
        self.port = port
        self.connected = False
        self.transport = None
        self.protocol = None
        self.keep_connect_flag = True
        self.on_con_lost = None
        self.lock = Lock()
        self.loop = None
        self.number = 0

    async def _connect(self):
        self.loop = asyncio.get_event_loop()
        self.on_con_lost = self.loop.create_future()
        self.transport, self.protocol = await self.loop.create_connection(
            lambda: ClientProtocol(self.on_con_lost, self.change_connect_state),
            self.ip, self.port)
        # 客户端用的是loop.create_connection
        self.connected = True
        try:
            await self.on_con_lost
        finally:
            if self.connected:
                self.transport.close()
                self.connected = False
                self.protocol = None

    def keep_connect(self):
        """
        保持连接
        :return:
        """
        def connect():
            while self.keep_connect_flag:
                try:
                    asyncio.run(self._connect())
                except Exception as e:
                    print(e)
                self.loop.close()
                time.sleep(1)
        Timer(0.1, connect).start()

    def close_connect(self):
        """关闭连接"""
        self.keep_connect_flag = False
        self.connected = False
        self.transport.close()

    def read(self, melsec_element: MelsecElement, start_addr, length=1):
        """
        读取PLC数据
        :param melsec_element: 软元件类型
        :param start_addr: 起始地址
        :param length: 长度
        :return: dic
        """
        while not self.connected:
            time.sleep(1)
        res_que = SimpleQueue()
        num = self.get_number()
        data = get_read_bytes_4e(num, melsec_element, start_addr, length)
        print(''.join(["%02X" % b for b in data]))
        self._data_write(num, res_que, data, True)
        try:
            res = res_que.get(timeout=6)
        except Exception:
            if self.connected:
                self.protocol.rm_response_data_mode_que(num)
            res = {'res': None, 'code': -1, 'desc': 'response timeout'}
        bts = res.get('res', [])
        if isinstance(bts, bytes):
            if melsec_element.m_nSub_cmd:
                res_bt = []
                for bit in bts:
                    res_bt.append(bit >> 4)
                    res_bt.append(bit & 0x0F)
                res_bt = res_bt[:length]
                res['res'] = res_bt
            else:
                res['res'] = [hex(int.from_bytes(bts[i:i + 2], byteorder='little', signed=False)) for i in
                              range(0, len(bts), 2)]
        print(res)
        return res

    def get_number(self):
        with self.lock:
            self.number += 1
            if self.number > 65535:
                self.number = 0
            return self.number

    def write(self, melsec_element: MelsecElement, start_addr, data):
        """
        写PLC数据
        :param melsec_element: 软元件类型
        :param start_addr: 起始地址
        :param data: 数据
        :return: dic
        """

        while not self.connected:
            time.sleep(1)
        res_que = SimpleQueue()
        num = self.get_number()
        data = get_write_bytes_4e(num, melsec_element, start_addr, data)
        print(''.join(["%02X" % b for b in data]))
        self._data_write(num, res_que, data, False)
        try:
            res = res_que.get(timeout=6)
        except Exception:
            if self.connected:
                self.protocol.rm_response_data_mode_que(num)
            res = {'res': None, 'code': -1, 'desc': 'response timeout'}
        print(res)
        return res

    def _data_write(self, num, res_que, data, is_read):
        """
        数据传输
        :param num: 序列号
        :param res_que: 回复队列
        :param data: 传输数据
        :param is_read: 控制模式
        :return: None
        """
        self.protocol.set_response_data_mode_que(num, res_que, is_read)
        self.transport.write(data)

    def change_connect_state(self, state):
        self.connected = state

    def is_connected(self):
        """获取MC连接状态"""
        return self.connected

