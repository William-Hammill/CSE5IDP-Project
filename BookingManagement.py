from flask import Flask, render_template
import os
# from Classes import database
from bookingConfirm import appointments
import sqlite3
booking_application = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
@booking_application.route('/')
def home():
    return render_template('AppointmentViewer.html')
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_first TEXT,
            customer_last TEXT,
            appt_time TEXT,
            appt_date TEXT,
            pet_name TEXT,
            comments TEXT,
            appt_status INTEGER DEFAULT 1
        )
    ''')
    c.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_first TEXT,
                    customer_last TEXT,
                    customer_number INTEGER,
                    appt_time TEXT,
                    appt_date TEXT,
                    pet_name TEXT,
                    reminder_date TEXT,
                    appointment_id INTEGER,
                    FOREIGN KEY(appointment_id) REFERENCES appointments(id)
                )
            ''')
    conn.commit()
    conn.close()


def start_application():
    # booking_application.secret_key = 'password'  # Be cautious with hardcoded secrets in production
    # booking_application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database",
    # "booking.sqlite3")}' booking_application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # database.init_app(booking_application)
    booking_application.register_blueprint(appointments)
    init_db()  # initialize sqlite database
    # with booking_application.app_context():
    #    database.create_all()
    return booking_application


if __name__ == '__main__':
    application = start_application()
    application.run(debug=True, host='0.0.0.0', port=5000)
