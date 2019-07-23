#! /usr/bin/env python
# -*- coding: utf-8 -*-
import itchat
from flask import Flask
from flask import request
import json
import datetime
from threading import Thread
import time
from multiprocessing import Process
import os

def SentChatRoomsMsg(msg, IRoomName):
    iRoom = itchat.search_chatrooms(name=IRoomName)
    # if not iRoom:
    #     memberList = itchat.search_friends(name="3999")
    #     memberList.extend(itchat.search_friends(name="Mr.Liu                      🙃"))
    #     memberList.extend(itchat.search_friends("萤火"))
    #     time.sleep(10)
    #     new_iRoom_list = itchat.create_chatroom(memberList, IRoomName)
    #     iRoom_id = new_iRoom_list["ChatRoomName"]
    #     print('iRoom_id: %s' % iRoom_id)
    #     itchat.update_chatroom(iRoom_id, detailedMember=True)
    #     iRoom = itchat.search_chatrooms(name=IRoomName)
    #     print(iRoom)
    # if not iRoom:
    #     print('发送指定群组名字:%s,%s'%(IRoomName,iRoom[0]['UserName']))
    # else:
    #     print("iRoom: %s   iRoomName: %s"%(iRoom,IRoomName))
    #     print("无法发送到微信，默认发送到运维服务告警接收群")
    #     IRoomName="运维服务部报警接收群"
    #     iRoom = itchat.search_chatrooms(name=IRoomName)
    print(iRoom[0]['UserName'])
    rest=itchat.send_msg(msg=msg, toUserName=iRoom[0]['UserName'])
    print('发送指定群组后返回值：%s'%rest)
if __name__ == '__main__':

    itchat.auto_login(enableCmdQR=False, hotReload=True)
    SentChatRoomsMsg('test',"运维服务部报警接收群")
    SentChatRoomsMsg('test',"施工BG产品紧急问题处理群")
    # SentChatRoomsMsg('test',"PTC(cloudt)高可用保障群")