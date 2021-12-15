#!/bin/bash

nohup python3 -u UpbitAutoTrade.py &

tail -f ./nohup.out
