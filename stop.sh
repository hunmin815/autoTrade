#!/bin/bash

PID=$(ps -ef | grep UpbitAutoTrade.py | head -n1 | awk {'print $2'})
echo $(ps -ef | grep UpbitAutoTrade.py | head -n1)
echo $PID
kill -9 $PID
echo "==kill check=="
echo $(ps -ef | grep UpbitAutoTrade.py)
echo "==UpbitAutoTrade Stop=="
echo "[$(date)] ==!UpbitAutoTrade Stop!==" >>./nohup.out
