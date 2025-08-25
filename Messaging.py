from twilio.rest import Client
# from flask import request, app
from twilio.twiml.messaging_response import MessagingResponse


# create twilio client/ message
def send_message(contents, number):
    account_sid = ''
    acc_token = ''
    message_client = Client(account_sid, acc_token)
    confirm_message = message_client.messages.create(body=contents,
                                                     from_='+12674294612',  # twilio number
                                                     to=number),
    return confirm_message.sid


# @app.route("/sms", methods=['GET', 'POST'])
def receive_message():
    response = MessagingResponse
    return str(response)


def send_placeholder(contents, number):
    account_sid = ''
    acc_token = ''
    message_client = Client(account_sid, acc_token)
    confirm_message = message_client.messages.create(body=contents,
                                                     from_='+12674294612',  # twilio number
                                                     to=number),
    return "message has been sent"


def recieve_placeholder():
    return 'Y'
