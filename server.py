import os, sys
from flask import Flask, request
from pymessenger import Bot
from pprint import pprint

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "[INSERT YOUR PAGE ACCESS TOKEN HERE]"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "[INSERT YOUR VERIFICATION TOKEN HERE]"

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello World", 200


@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  pprint(data)
  data = dict([(str(k), v) for k, v in data.items()])
  
  if data['object'] == 'page':
    for entry in data['entry']:
      messaging = entry['messaging']
      for messaging_event in messaging:
        sender_id = messaging_event['sender']['id']
        recipient_id = messaging_event['recipient']['id']
        
        # Echo Bot
        if messaging_event.get('message'):
          if messaging_event['message'].get('text'):
            # Retrieve the message
            response = messaging_event['message']['text']
            # Echo the message
            bot.send_text_message(sender_id, response)
  
  return 'ok', 200

if __name__ == "__main__":
	app.run()
