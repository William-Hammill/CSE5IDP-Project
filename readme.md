## CSE5IDP appointment booking system

Note: Python version must be 3.12(.11) or earlier in order to be compatible with the previous project's application, else it will not work.

This is a flask based system to allow the employees of a pet grooming business to automate their booking system.

This system is intended to allow customers to easily book their own appointments then confirm them via a text message sent using Twilio SMS.
this message will allow customers to confirm or cancel their appointments while also reminding them. however rescheduling will instead be done via phone calls.

This system also requires a Twilio account for messaging functions to work, see Messaging.py file for more information

Running this webapp:

pip install flask

python app.py
