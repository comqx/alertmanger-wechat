#!/usr/bin/env python
#-*- coding: utf-8 -*-
# writer:lqx
import itchat
from flask import Flask
from flask import request
import json
import datetime
from threading import Thread
import time
from multiprocessing import Process
#发送恢复信息  v7


def SentChatRoomsMsg(msg,cluster):
    iRoom = itchat.search_chatrooms(name=cluster)
    if not iRoom:
        memberList=itchat.search_friends(name="3999")
        memberList.extend(itchat.search_friends(name="Mr.Liu                      🙃"))
        memberList.extend(itchat.search_friends("萤火"))
        time.sleep(10)
        new_iRoom_list=itchat.create_chatroom(memberList,cluster)
        iRoom_id=new_iRoom_list["ChatRoomName"]
        print('iRoom_id: %s'%iRoom_id)
        itchat.update_chatroom(iRoom_id,detailedMember=True)
        iRoom = itchat.search_chatrooms(name=cluster)
        print(iRoom)
    itchat.send_msg(msg=msg, toUserName=iRoom[0]['UserName'])


#数据格式化
def transform(data_from_am):
    count=1
    fire_msg=""
    time_now = time.strftime('%Y-%m-%d %X')
    for alert in data_from_am['alerts']:
        level = alert["labels"].get("severity")
        cluster = alert["labels"].get("cluster")
        if alert.get("status") == "firing":
            status="触发报警"
        elif alert.get("status") == "resolved":
            status = "已经恢复"
        else:
            status ="没有获取到状态"
        if not  cluster:
          cluster="default-alert-iRoom"
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
                   "环境： {0}\n".format(cluster) + \
                    "问题状态： {0}\n".format(status) + \
                    "告警级别： {0}\n".format(level) + \
                           "报警名称:  {} \n".format(alertname) + \
                           "报警名称空间： {}\n".format(namespace) +\
                           "pod所在机器： {}\n".format(host_ip) +\
                           "报警详细信息:  {} \n".format(annotations_msg) + \
                           "开始时间:  {} \n".format(time_start) + \
                           "当前时间:  {} \n".format(time_now)
        count+=1
    return fire_msg,cluster



app = Flask(__name__)
#接收alertmanager的报警数据
@app.route('/v2/alertmanager/post', methods=['POST'])
def send():
    print(request.method)
    if request.method == 'POST':
        print("开始处理 alertmanager 告警: ")
        post_data = request.get_data()
        post_data = post_data.decode('utf-8')
        print("时间：%s 收到json数据： %s" %(time.strftime('%Y-%m-%d %X'),post_data))
        data_dict = json.loads(post_data)
        try:
            send_data,cluster=transform(data_dict) #数据格式化
        except Exception as a:
            print('数据格式化出现问题。。。:',a)
        try:
            print('发送微信指定群组')
            SentChatRoomsMsg(send_data,cluster)
        except Exception as e:
            print('发送微信指定群组出现问题:',e)
        try:
            time.sleep(5)
            cluster='test'
            print('发送微信群test')
            SentChatRoomsMsg(send_data,cluster)
        except Exception as e:
            print('发送微信群test出现问题:',e)
    return "succeed"


if __name__ == '__main__':
#    itchat.auto_login(enableCmdQR=False,hotReload=False)
    itchat.auto_login(enableCmdQR=False,hotReload=True,statusStorageDir='itchat.pkl')
    # P1=Process(target =app.run(host='0.0.0.0', port=8099)) #开启线程运行flask
    # P1.start()
    ti=Thread(target=app.run(host='0.0.0.0', port=8088)) #开启线程运行flask
    ti.start()
    itchat.run()
