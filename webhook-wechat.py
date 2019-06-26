#!/usr/bin/env python
# -*- coding: utf-8 -*-
# writer:lqx
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
    if not iRoom:
        memberList = itchat.search_friends(name="3999")
        memberList.extend(itchat.search_friends(name="Mr.Liu                      🙃"))
        memberList.extend(itchat.search_friends("萤火"))
        time.sleep(10)
        new_iRoom_list = itchat.create_chatroom(memberList, IRoomName)
        iRoom_id = new_iRoom_list["ChatRoomName"]
        print('iRoom_id: %s' % iRoom_id)
        itchat.update_chatroom(iRoom_id, detailedMember=True)
        iRoom = itchat.search_chatrooms(name=IRoomName)
        print(iRoom)
    print('发送指定群组名字:%s,%s'%(IRoomName,iRoom[0]['UserName']))
    rest=itchat.send_msg(msg=msg, toUserName=iRoom[0]['UserName'])
    print('发送指定群组后返回值：%s'%rest)

#找到集群名和微信群的对应关系
def CustomIRoomName(ClusterName):
    CustomIRoomNameDict=json.loads(os.getenv('CustomIRoomNameJson'))
    # {"ptc-ywd-pro-hbali":"云文档","ptc-yw-pro-hbali":"云文档","NullClusterName":""}
    if ClusterName in CustomIRoomNameDict:
        IRoomName = CustomIRoomNameDict['ClusterName']
    else:
        IRoomName=ClusterName
    return IRoomName

# 数据格式化
def transform(post_data):
    data_dict = json.loads(post_data)
    count = 1
    fire_msg = ""
    time_now = time.strftime('%Y-%m-%d %X')
    for alert in data_dict['alerts']:
        level = alert["labels"].get("severity")
        ClusterName = alert["labels"].get("cluster")
        if alert.get("status") == "firing":
            status = "触发报警"
        elif alert.get("status") == "resolved":
            status = "已经恢复"
        else:
            status = "没有获取到状态"
        if not ClusterName:
            ClusterName = "NullClusterName"
        alertname = alert["labels"].get("alertname")
        namespace = alert["labels"].get("namespace")
        host_ip = alert["labels"].get("host_ip")
        if not host_ip:
            host_ip = alert["labels"].get("instance")
        if not host_ip:
            host_ip = alert["labels"].get("node")
        if alert.get("annotations"):
            annotations_msg = alert["annotations"].get("message")
        time_start = alert["startsAt"].split(".")[0]
        # time_start=datetime.datetime.strptime(time_start,'%Y-%m-%dT%H:%M:%S')+ datetime.timedelta(hours=8)
        fire_msg += "---------第 {} 条---------\n".format(count) + \
                    "环境： {0}\n".format(ClusterName) + \
                    "问题状态： {0}\n".format(status) + \
                    "告警级别： {0}\n".format(level) + \
                    "报警名称:  {} \n".format(alertname) + \
                    "报警名称空间： {}\n".format(namespace) + \
                    "pod所在机器： {}\n".format(host_ip) + \
                    "报警详细信息:  {} \n".format(annotations_msg) + \
                    "开始时间:  {} \n".format(time_start) + \
                    "当前时间:  {} \n".format(time_now)
        count += 1
        IRoomName=CustomIRoomName(ClusterName)
    return fire_msg, IRoomName

app = Flask(__name__)
# 接收alertmanager的报警数据
@app.route('/v2/alertmanager/post', methods=['POST'])
def send():
    print(request.method)
    if request.method == 'POST':
        print("开始处理 alertmanager 告警: ")
        post_data = request.get_data()
        post_data = post_data.decode('utf-8')
        print("时间：%s 收到json数据： %s" % (time.strftime('%Y-%m-%d %X'), post_data))
        try:
            send_data, IRoomName = transform(post_data)  # 数据格式化
        except Exception as err:
            print('数据格式化出现问题:%s，问题数据：%s'%(err,post_data))

        try:
            SentChatRoomsMsg(send_data, IRoomName)
        except Exception as e:
            print('发送微信指定群组出现问题:', e)
        time.sleep(5)
        if IRoomName != '运维服务部报警接收群':
            IRoomName = '运维服务部报警接收群'
            SentChatRoomsMsg(send_data, IRoomName)
    return "succeed"


if __name__ == '__main__':
    #    itchat.auto_login(enableCmdQR=False,hotReload=False)
    import platform
    if platform.system() == "Windows":
        itchat.auto_login(enableCmdQR=False, hotReload=True, statusStorageDir='itchat.pkl')
        print('获取变量成功',json.loads(os.getenv('CustomIRoomNameJson')))
    else:
        itchat.auto_login(enableCmdQR=True, hotReload=True, statusStorageDir='itchat.pkl')
        print('获取变量成功', json.loads(os.getenv('CustomIRoomNameJson')))
    # P1=Process(target =app.run(host='0.0.0.0', port=8099)) #开启线程运行flask
    # P1.start()
    ti=Thread(target=app.run(host='0.0.0.0', port=8088)) #开启线程运行flask
    ti.start()
    itchat.run()



