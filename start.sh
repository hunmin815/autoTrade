#!/bin/bash

nohup python3 -u UpbitAutoTrade.py &

tail -f $env_autoTrade_Dir./nohup.out
