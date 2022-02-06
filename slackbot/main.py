from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
BOT_USER_TOKEN = "xoxb-3062362679586-3062373690386-VVqLHe6283JdxAH7cGMAuVCi"
USER_TOKEN = "xoxp-3062362679586-3062382830131-3059488232357-d7b342ee6218c9255d29aa7456b45168"
swc = WebClient(token=BOT_USER_TOKEN)
EVENT_TOKEN = "15c23c1f9950849f957f05567d354750"
sea = SlackEventAdapter(EVENT_TOKEN, "/slack/events", app)

MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "",
    },
}

@sea.on("message")
def message(payload):
    channel = payload.get("event").get("channel")
    MESSAGE_BLOCK["text"]["text"] = "Hello World!"
    to_send = {"channel": channel, "blocks": [MESSAGE_BLOCK]}

    print("Sending message...")
    return swc.chat_postMessage(**to_send)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)