from slack_sdk import WebClient

with open('SlackData/token.txt', 'r') as f:
    TOKEN = f.readline().strip()
with open('SlackData/channel.txt', 'r') as f:
    CHANNEL = f.readline().strip()

def sendTextWithLink(text:str, link:str) -> None:
    client = WebClient(token = TOKEN)
    client.chat_postMessage(
        channel=CHANNEL,
        text = text + "\n" + link + "&siteGubun=1&menuGubun=1"
    )
