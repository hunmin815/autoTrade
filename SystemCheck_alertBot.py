import requests
import datetime
import os

# 메시지 전송 함수
def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


def nowtime():
    now = datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S")  # 현재 DateTime
    return now


myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID

try:
    post_message(myToken, myChannel, " ")
    post_message(
        myToken,
        myChannel,
        "$$🔌🟢 Trading System Alive$$\nServer Time : " + str(nowtime()),
    )
except:
    post_message(myToken, myChannel, " ")
    post_message(
        myToken,
        myChannel,
        "!!🏴‍☠️❗🔴 Trading System Dead!!\nServer Time : " + str(nowtime()),
    )
