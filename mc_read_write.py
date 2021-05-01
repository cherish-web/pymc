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
    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost
        self.connected = False
        self.response_data_queue = SimpleQueue()
        self.transport = None

    def connection_made(self, transport: Transport) -> None:
        self.connected = True
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        self.response_data_queue.put(data)

    def connection_lost(self, exc):
        print('服务器连接断开')
        self.connected = False
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

    async def _connect(self):
        self.loop = asyncio.get_event_loop()
        self.on_con_lost = self.loop.create_future()
        self.transport, self.protocol = await self.loop.create_connection(
            lambda: ClientProtocol(self.on_con_lost),
            self.ip, self.port)
        # 客户端用的是loop.create_connection
        self.connected = True
        try:
            await self.on_con_lost
        finally:
            if self.connected:
                self.transport.close()
                self.connected = False

    def keep_connect(self):
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
        while not self.protocol:
            time.sleep(1)
        data = get_read_bytes(melsec_element, start_addr, length)
        print(''.join(["%02X" % b for b in data]))
        res = self._data_write(data, True)
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

    def write(self, melsec_element: MelsecElement, start_addr, data):
        """
        写PLC数据
        :param melsec_element: 软元件类型
        :param start_addr: 起始地址
        :param data: 数据
        :return: dic
        """
        while not self.protocol:
            time.sleep(1)
        data = get_write_bytes(melsec_element, start_addr, data)
        print(''.join(["%02X" % b for b in data]))
        res = self._data_write(data, False)
        print(res)
        return res

    def _data_write(self, data, is_read):
        with self.lock:
            self.transport.write(data)
            res_data = bytes()
            while True:
                try:
                    res_data += self.protocol.response_data_queue.get(timeout=6)
                except Exception:
                    return {'res': None, 'code': -1, 'desc': 'response timeout'}
                respond_code = get_respond_code(res_data)
                if respond_code == -1:
                    continue
                elif respond_code > 0:
                    return {'res': None, 'code': respond_code, 'desc': f'mc {"read" if is_read else "write"} error'}
                if is_read:
                    res_data = get_read_respond(res_data)
                else:
                    res_data = get_write_respond(res_data)
                if res_data is not None:
                    return {'res': res_data, 'code': respond_code, 'desc': ''}

    def is_connected(self):
        """获取MC连接状态"""
        return self.connected

