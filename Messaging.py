from twilio.rest import Client
from flask import request
from twilio.twiml.messaging_response import MessagingResponse


def send_message(contents, number):
    account_id = ''
    acc_token = ''
    message_client = Client(account_id, acc_token)
    confirm_message = message_client.messages.create(body=contents, from_='', to=number)
    return confirm_message.ssid


# @app.route("/sms", methods=['GET', 'POST'])
def receive_message():
    # account_id = ''
    # acc_token = ''
    # message_client = Client(account_id, acc_token)
    message_response = request.form['Body}']

    return message_response
