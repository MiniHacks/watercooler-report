from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import requests
import sentence_splitter

app = Flask(__name__)
BOT_USER_TOKEN = "xoxb-3062362679586-3062373690386-VVqLHe6283JdxAH7cGMAuVCi"
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

ML_ENDPOINT = "localhost:8000/process_segments"
THRESHOLD = 0.85
ADMIN_ID = "U031UB8QE3V"

def get_real_name(user_id):
    response = swc.users_profile_get(user=user_id)
    return response.data.get("profile").get("real_name")

def alert_admin(name, segment, certainty):
    MESSAGE_BLOCK["text"]["text"] = "{name}'s message was flagged for harrassment. Please review the follow message: \n`\"{segment}\"`\n The system is {certainty}% certain this was inapporiate comment.".format(name=name, segment=segment.strip(), certainty=certainty * 100)
    to_send = {"channel": ADMIN_ID, "blocks": [MESSAGE_BLOCK]}
    result = swc.chat_postMessage(**to_send)
    return result

@sea.on("message")
def message(payload):
    event = payload.get("event")
    if event.get("bot_id") != None:
        return

    text = event.get("text")
    channel = event.get("channel")

    # sentences = sentence_splitter.split_into_sentences(text)
    # response = requests.post(ML_ENDPOINT, json={"segments": sentences})
    # print(response)

    # response = response.json()
    # for segment, certainty in response["result"]:
    #     if certainty > THRESHOLD:
    #         name = get_real_name(event.get("user"))
    #         alert_admin(name, segment, certainty)
    alert_admin("Someone", "Booty", 0.9)

    MESSAGE_BLOCK["text"]["text"] = "Hello World!"
    to_send = {"channel": channel, "blocks": [MESSAGE_BLOCK]}

    print("Sending message...")
    result = swc.chat_postMessage(**to_send) 
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)