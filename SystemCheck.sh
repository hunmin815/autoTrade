#!/bin/sh

cd $env_autoTrade_Dir

python3 SystemCheck_alertBot.py || python SystemCheck_alertBot.py

exit 0
