#!/usr/bin/env python
# coding:utf-8

# Messenger API integration
# We assume you have:
# * a Wit.ai bot setup (https://wit.ai/docs/quickstart)
# * a Messenger Platform setup (https://developers.facebook.com/docs/messenger-platform/quickstart)
# You need to `pip install the following dependencies: requests, bottle.
#
# 1. pip install requests bottle
# 2. run this app on a cloud service provider Heroku
#    Note that webhooks must have a valid SSL certificate, signed by a certificate authority and won't work on your localhost.
# 3. Set your environment variables e.g. WIT_TOKEN=your_wit_token
#                                        FB_PAGE_TOKEN=your_page_token
#                                        FB_VERIFY_TOKEN=your_verify_token
# 4. Run your server e.g. python examples/app.py {PORT}
# 5. Subscribe your page to the Webhooks using verify_token and `https://<your_host>/webhook` as callback URL.
# 6. Talk to your bot on Messenger!

import os
import json
import requests
import logging
#import sys
from sys import argv
from wit import Wit
from bottle import Bottle, request, debug

# Wit.ai parameters
WIT_TOKEN = os.environ.get('WIT_TOKEN')
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
# Unknown user request
UNKNOWN_REQ = os.environ.get('UNKNOWN_REQ')

# Setup Bottle Server
debug(True)
app = Bottle()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Facebook Messenger GET Webhook
@app.get('/webhook')
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.query.get('hub.verify_token')
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.query.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.post('/webhook')
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    unknowreq = os.environ.get('UNKNOWN_REQ')

    print("+++ Recieved message from user ", data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                if messaging_event.get('message') and messaging_event['message'].get('text'):  # someone sent us a message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        client.run_actions(session_id=sender_id, message=message_text)
                else:
                    fb_message(sender_id, unknowreq) # unknown request recieved from user

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pring ("++++ Recieved postback")
                        recipient_id = messaging_event["recipient"]["id"]
                        postback = messaging_event["postback"].get("payload")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass



                return None

def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    print ('++++ in fb_message function ', text)
    params = {
        "access_token": os.environ["FB_PAGE_TOKEN"]
    }

    headers = {
        "Content-Type": "application/json"
    }

    msgdata = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": text
        }
    })

    print(">>> Message sent: ", msgdata)

    # call facebook messenger api
    invokeFBapi(params, headers, msgdata)


def buildresponse(sender_id, response):
    """
    buildresponse function
    """

    print('++++ in buildresponse func - quickreplies Response :',  response['text'].decode('UTF-8') + '\nQR: ' + ', '.join(response['quickreplies']))
    print(">>> Opciones: {}".format(response['quickreplies']))

    text = response['text']
    msgdata = {}
    recipient = {};
    message = {}
    recipient["id"] = sender_id;

    message["text"] = response['text']
    message["quickreplies"] = json.dumps(response['quickreplies'])

    msgdata["recipient"] = recipient
    msgdata["message"] = message

    print (">>> Message msgdata", json.dumps(msgdata))

    params = {
        "access_token": os.environ["FB_PAGE_TOKEN"]
    }

    headers = {
        "Content-Type": "application/json"
    }

    msgdata2 = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message":{
        "text":text,
        "quick_replies":[
          {
            "content_type":"text",
            "title":"כן",
            "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_YES"
          },
          {
            "content_type":"text",
            "title":"לא",
            "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_NO"
          }
        ]
      }
    })

    print (">>> Message msgdata2", msgdata2)

    invokeFBapi(params, headers, msgdata2)



def invokeFBapi(params, headers, data):
    """
    Facebook messenger api callback invoke
    """

    resp = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers , data=data)

    if resp.status_code != 200:
        log(resp.status_code)
        log(resp.text)

    return resp.content




def send(request, response):
    """
    Sender function
    """
    fb_id = request['session_id']

    if response['quickreplies']:
        buildresponse(fb_id, response)
    else:
        text = response['text']
        fb_message(fb_id, text)

def log(messages):  # simple wrapper for logging to stdout on heroku
    print str(messages)


# Setup Actions for Wit
actions = {
    'send': send
}

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)

# set logger level for Wit.ai client
client.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0', port=argv[1])
