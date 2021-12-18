import sys
import requests
import datetime
import os
import sys


def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID
ProcessStatus = str(sys.argv[1]) # 프로세스 상태 코드 (매개 변수)

try:
  if ProcessStatus == "ok":
    now = datetime.datetime.now()
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "$$📈 Trading Process Alive$$")
    post_message(myToken, myChannel, "Server Time : " + str(now))

  elif ProcessStatus == "dead":
    now = datetime.datetime.now()
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "!!🏴‍☠️ Trading Process Dead!!")
    post_message(myToken, myChannel, "Server Time : " + str(now))

  elif ProcessStatus == "restart":
    now = datetime.datetime.now()
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "🔧 Restarting Now ...")
    post_message(myToken, myChannel, "Server Time : " + str(now))

  else:
    now = datetime.datetime.now()
    post_message(myToken, myChannel, " ")
    post_message(myToken, myChannel, "❗ Sorry, Restarting Fail ... Please Check Process")
    post_message(myToken, myChannel, "Server Time : " + str(now))

except Exception as e:
    print(e)
