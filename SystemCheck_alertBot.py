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


myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID

try:
    now = datetime.datetime.now() # 현재 DateTime
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "$$Trading System Alive$$")
    post_message(myToken, myChannel, "Server Time : " + str(now))
except:
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "!!Trading System Dead!!")
