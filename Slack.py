import requests

with open('SlackData/token.txt', 'r') as f:
    TOKEN = f.readline()
with open('SlackData/channel.txt', 'r') as f:
    CHANNEL = f.readline()

def sendTextWithLink(text:str, link:str) -> None:
    URL = "https://slack.com/api/chat.postMessage"
    data = {"token":TOKEN, "channel":CHANNEL, "text": text + "\n" +link}
    res = requests.post(URL, data=data)
    print(res.text)