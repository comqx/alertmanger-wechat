#!/usr/bin/env python
#-*- coding: utf-8 -*-
# writer:lqx
import os
import json
import time
namespace ='''
{"receiver":"webhook","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"Deployment_Replicas_Mismatch","cluster":"ptc-yw-pro-hbali","deployment":"aliacs-service-catalog-catalog-controller-manager","endpoint":"http","instance":"172.18.2.89:8080","job":"kube-state-metrics","namespace":"catalog","pod":"ops-prometheus-kube-state-metrics-65696f959-2f7s5","prometheus":"glodon-ops/operator-prometheus","service":"ops-prometheus-kube-state-metrics","severity":"critical"},"annotations":{"message":"Deployment aliacs-service-catalog-catalog-controller-manager has not matched the expected number of replicas for longer than an hour."},"startsAt":"2019-07-02T21:12:46.20994256+08:00","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prometheus-ptc-yw-pro-hbali.glodon.com/graph?g0.expr=kube_deployment_spec_replicas%7Bjob%3D%22kube-state-metrics%22%7D+%21%3D+kube_deployment_status_replicas_available%7Bjob%3D%22kube-state-metrics%22%7D\u0026g0.tab=1"},{"status":"firing","labels":{"alertname":"Pod_Crash_Looping","cluster":"ptc-yw-pro-hbali","container":"controller-manager","endpoint":"http","instance":"172.18.2.89:8080","job":"kube-state-metrics","namespace":"catalog","pod":"aliacs-service-catalog-catalog-controller-manager-784fb5f4dd5hj","prometheus":"glodon-ops/operator-prometheus","service":"ops-prometheus-kube-state-metrics","severity":"critical"},"annotations":{"message":"当前 aliacs-service-catalog-catalog-controller-manager-784fb5f4dd5hj 15分钟之内出现连续重启"},"startsAt":"2019-07-02T20:28:01.20994256+08:00","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prometheus-ptc-yw-pro-hbali.glodon.com/graph?g0.expr=rate%28kube_pod_container_status_restarts_total%7Bjob%3D%22kube-state-metrics%22%7D%5B8m%5D%29+%2A+60+%2A+5+%3E+0\u0026g0.tab=1"},{"status":"resolved","labels":{"alertname":"Pod_Restart","cluster":"ptc-yw-pro-hbali","container":"controller-manager","endpoint":"http","host_ip":"10.126.1.97","instance":"172.18.2.89:8080","job":"kube-state-metrics","namespace":"catalog","pod":"aliacs-service-catalog-catalog-controller-manager-784fb5f4dd5hj","prometheus":"glodon-ops/operator-prometheus","service":"ops-prometheus-kube-state-metrics","severity":"critical"},"annotations":{"message":"当前 aliacs-service-catalog-catalog-controller-manager-784fb5f4dd5hj  最近5分钟出现重启."},"startsAt":"2019-07-09T18:58:16.20994256+08:00","endsAt":"2019-07-09T19:03:01.20994256+08:00","generatorURL":"http://prometheus-ptc-yw-pro-hbali.glodon.com/graph?g0.expr=changes%28kube_pod_container_status_restarts_total%7Bjob%3D%22kube-state-metrics%22%7D%5B5m%5D%29+%2A+on%28namespace%2C+pod%29+group_left%28host_ip%29+%28node_namespace_pod%3Akube_pod_info%3A%29+%21%3D+0\u0026g0.tab=1"}],"groupLabels":{"cluster":"ptc-yw-pro-hbali","namespace":"catalog"},"commonLabels":{"cluster":"ptc-yw-pro-hbali","endpoint":"http","instance":"172.18.2.89:8080","job":"kube-state-metrics","namespace":"catalog","prometheus":"glodon-ops/operator-prometheus","service":"ops-prometheus-kube-state-metrics","severity":"critical"},"commonAnnotations":{},"externalURL":"http://federation.glodon.com","version":"4"}
'''
def CustomIRoomName(ClusterName):
    jsn = '{"ptc-yw-pro-hbali":"运维服务部报警接收群","NullClusterName":"运维服务部报警接收群","sg-project-pro-hbali":"施工BG产品紧急问题处理群","sg-platform-test-hbali":"PTC(cloudt)高可用保障群","sg-project-test-hbali":"施工BG产品紧急问题处理群","sg-xz-pro-hbali":"PTC(cloudt)高可用保障群","sg-pfpt-pro-hbhw":"PTC(cloudt)高可用保障群"}'
    CustomIRoomNameDict=json.loads(jsn)
    if ClusterName in CustomIRoomNameDict:
        IRoomName = CustomIRoomNameDict[ClusterName]
    else:
        IRoomName="运维服务部报警接收群"
    return IRoomName
def transform(post_data):
    data_dict = json.loads(post_data)
    count = 1
    fire_msg = ""
    time_now = time.strftime('%Y-%m-%d %X')
    defClusterName=data_dict['groupLabels'].get("cluster")
    defnamespace=data_dict['groupLabels'].get("namespace")
    for alert in data_dict['alerts']:
        level = alert["labels"].get("severity")
        if level == 'critical':
            level+=' [发怒]'
        ClusterName = alert["labels"].get("cluster")
        if alert.get("status") == "firing":
            status = "触发报警 [惊恐]"
        elif alert.get("status") == "resolved":
            status = "已经恢复 [愉快]"
        else:
            status = "没有获取到状态[疑问]"
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
            if  not annotations_msg:
                annotations_msg = alert["annotations"].get("description")
        time_start = alert["startsAt"].split(".")[0]
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
    IRoomName = CustomIRoomName(defClusterName)
    if defnamespace in ["glodon-ops", "kube-system", None] or 'cattle' in defnamespace:
        IRoomName = "运维服务部报警接收群"
    return fire_msg, IRoomName

a,b=transform(namespace)
print(a)
print(b)