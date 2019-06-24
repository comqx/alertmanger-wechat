#!/bin/sh


sed -i "s#{RoomName}#$RoomName#g" ./webhook-wechat.py
python3 webhook-wechat.py

