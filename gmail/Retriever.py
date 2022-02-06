# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import os.path
import base64
import requests
from bs4 import BeautifulSoup
from re import sub
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

ML_ENDPOINT = "http://34.67.45.8/process_segments"
ADMIN = "lee02802@umn.edu"
USER = "andrewhoyle@watercoolerreport.tech"
THRESHOLD = 0.4


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose']

# Parses the body for most words
def parse(body):
    body = sub(r'(\[<p>|</p>\])', '', body)
    body, text = body.split('\n'), ""
    for i, line in enumerate(body):
        body[i] = line.rstrip()
        if len(body[i]) > 0:
            text += body[i] + " "
    return text

# Determines if the body of the message reaches a thresold that would
# incidates some form of sexual harassment.
def determine(service, body, fromUser):
    name = None
    response = requests.get(ML_ENDPOINT, data=json.dumps([body]))
    response = response.json()
    for cur in response["result"]:
        certainty = cur["rating"]
        segment = cur["segment"]
        if certainty > THRESHOLD:
            certainty *= 100
            certainty = round(certainty, 2)
            name = fromUser
            send_message(service, create_message(fromUser, segment, certainty))
            break
    return name

def create_message(name, segment, certainty):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message_text = f"We've flagger {name}'s message for sexual harassment with {certainty}% certainty: \n`\"{segment}\"`\n If you deem this to be a case of sexual harassment, look to www.rainn.org/, www.womenagainstabuse.org/, leanin.org/ for resources.".format(name=name, segment=segment.strip(), certainty=certainty * 100)
  message = MIMEText(message_text)
  message['to'] = ADMIN
  message['from'] = USER
  message['subject'] = "Report - Misconduct"
  # print(message.as_string())
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode()}

def send_message(service, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  # try:
  message = (service.users().messages().send(userId='me', body=message)
              .execute())
  print('Message Id: %s' % message['id'])
  return message
  # except HttpError as error:
  #   print('An error occurred: %s' % error)


def main():
    creds = None
    # Checks for token.json in path.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Make sure creds actually is initialized 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # this will get the name and email cleanly
    # msg_res = service.users().messages()
    # results = msg_res.list(userId='me', maxResults=10).execute()
    # messages = results.get('messages', [])
    # if not messages:
    #     print('No messages found.')
    # else:
    #     print('Message from:')
    # for msg in messages:
    #     msg_dict = msg_res.get(userId='me', id=msg['id']).execute()
    #     msg_headers = msg_dict['payload']['headers']
    #     msg_from = filter(lambda hdr: hdr['name'] == 'From', msg_headers)
    #     msg_from = list(msg_from)[0]
    #     print(msg_from['value'])
    
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
  
        try:
            payload = txt['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'From':
                    sender = d['value']
  
            if payload.get('parts') is None:
                continue
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            # Now, the data obtained is in lxml. So, we will parse 
            # it with BeautifulSoup library
            try:
                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.body()
            except Exception as e:
                continue
  
            # Parse it down to smaller components
            body = parse(str(body))
            if determine(service, body, sender):
                return
            

        except HttpError as error:
            print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()