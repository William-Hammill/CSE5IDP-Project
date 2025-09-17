from flask import request
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


# create twilio client/ message
def send_message(contents, number):
    account_sid = '' # remove before committing/pushing to GitHub
    acc_token = ''  # remove before committing/pushing to GitHub
    message_client = Client(account_sid, acc_token)
    confirm_message = message_client.messages.create(body=contents,
                                                     from_='+12674294612',  # twilio number
                                                     to=number)

    #response = receive_message()
    #return str(response)
    return confirm_message.sid


# @app.route("/sms", methods=['GET', 'POST'])
def receive_message():
    account_sid = os.environ[""]
    auth_token = os.environ[""]
    client = Client(account_sid, auth_token)

    message = client.messages("MGdd3583909790c7d6adbf9e8a42d19f58").fetch()

    #print(message.body)
    response = MessagingResponse()
    contents = request.form['body']
   # response.message()
    return contents
    #return str(response.message())


#def send_placeholder(contents, number):
   # account_sid = ''
    #acc_token = ''
    #message_client = Client(account_sid, acc_token)
    #confirm_message = message_client.messages.create(body=contents,
     #                                                from_='+12674294612',  # twilio number
     #                                                to=number),
 #  print(contents)
 #  return "message has been sent"


#def recieve_placeholder():
#    return 'Y'
