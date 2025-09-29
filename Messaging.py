from twilio.rest import Client


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
def receive_message(client_num):
    account_sid = ''
    acc_token = ''
    message_client = Client(account_sid, acc_token)
    received_messages = message_client.messages.list(from_=client_num, to='+12674294612', limit=1)

    message = received_messages[0]
    return message.body
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
