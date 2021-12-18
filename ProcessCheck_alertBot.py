import requests
import datetime
import os

# os.system("C:\stockauto\\test.py") #다른 파이썬 파일 실행 코드

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID

try:
  now = datetime.datetime.now()
  post_message(myToken,myChannel, " ")
  post_message(myToken,myChannel,"$$Trading Process Alive$$")
  post_message(myToken,myChannel,"Server Time : "+str(now))
except:
  post_message(myToken,myChannel, " ")
  post_message(myToken,myChannel,"!!Trading Process Dead!!")
  post_message(myToken,myChannel,"Server Time : "+str(now))