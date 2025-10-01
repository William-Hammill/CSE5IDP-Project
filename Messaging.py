from twilio.rest import Client


# create twilio client/ message for sending
def send_message(contents, number):
    account_sid = ''  # Must be filled in for code to function
    acc_token = ''  # Must be filled in for code to function
    message_client = Client(account_sid, acc_token)
    confirm_message = message_client.messages.create(body=contents,
                                                     from_='+12674294612',  # twilio number
                                                     to=number)
    return confirm_message.sid


# create client for receiving messages
def receive_message(client_num):
    account_sid = ''  # Must be filled in for code to function
    acc_token = ''  # Must be filled in for code to function
    message_client = Client(account_sid, acc_token)
    received_messages = message_client.messages.list(from_=client_num, to='+12674294612', limit=1)

    message = received_messages[0]
    return message.body
