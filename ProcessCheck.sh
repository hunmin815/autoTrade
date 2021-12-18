#!/bin/sh

cd $env_autoTrade_Dir
PID1=$(ps -ef | grep UpbitAutoTrade.py | grep -v "grep" | awk {'print $2'} | head -n1)

ReStartup=0 # 재기동 여부

if [ -z $PID1 ]; then
  python3 ProcessCheck_alertBot.py dead || python ProcessCheck_alertBot.py dead
  sleep 1
  $(nohup python3 -u UpbitAutoTrade.py &) || $(nohup python -u UpbitAutoTrade.py &)
  sleep 1
  python3 ProcessCheck_alertBot.py restart || python ProcessCheck_alertBot.py restart
  ReStartup=1
else
  python3 ProcessCheck_alertBot.py ok || python ProcessCheck_alertBot.py ok
fi

sleep 3

if [ $ReStartup -eq 1 ]; then
  PID1=$(ps -ef | grep UpbitAutoTrade.py | grep -v "grep" | awk {'print $2'} | head -n1)

  if [ -z $PID1 ]; then
    python3 ProcessCheck_alertBot.py fail || python ProcessCheck_alertBot.py fail
  else
    python3 ProcessCheck_alertBot.py ok || python ProcessCheck_alertBot.py ok
  fi
fi

exit 0
