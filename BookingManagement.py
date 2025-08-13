from flask import Flask, render_template
import os
from Classes import database
from bookingConfirm import appointments

basedir = os.path.abspath(os.path.dirname(__file__))

def start_application():
    application=Flask(__name__)
    application.secret_key = 'password'  # Be cautious with hardcoded secrets in production
    application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database", "booking.sqlite3")}'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(application)
    application.register_blueprint(appointments)

    with application.app_context():
        database.create_all()

    return application

if __name__ =='__main__':
    application= start_application()
    application.run(debug=True, host='0.0.0.0', port= '8080')