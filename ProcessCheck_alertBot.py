import sys
import requests
import datetime
import os


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
ProcessStatus = str(sys.argv[1])  # 프로세스 상태 코드 (매개 변수)

try:
    if ProcessStatus == "ok":
        post_message(myToken, myChannel, " ")
        post_message(
            myToken,
            myChannel,
            "$$📈🟢 Trading Process Alive$$\nServer Time : " + str(nowtime()),
        )

    elif ProcessStatus == "dead":
        post_message(myToken, myChannel, " ")
        post_message(
            myToken,
            myChannel,
            "!!🏴‍☠️ Trading Process Dead!!\nServer Time : " + str(nowtime()),
        )

    elif ProcessStatus == "restart":
        post_message(myToken, myChannel, " ")
        post_message(
            myToken, myChannel, "🔧 Restarting Now ...\nServer Time : " + str(nowtime())
        )

    else:
        post_message(myToken, myChannel, " ")
        post_message(
            myToken,
            myChannel,
            "❗🔴 Sorry, Restarting Fail ... Please Check Process\nServer Time : "
            + str(nowtime()),
        )

except Exception as e:
    print(e)
