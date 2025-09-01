from flask import Flask, render_template
from datetime import datetime
from bookingConfirm import appointments
import sqlite3

booking_application = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
@booking_application.route('/')
def home():
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    booked_appointments = c.fetchall()
    conn.close()
    #current_datetime = datetime.now()
   #current_time = current_datetime.time()
    #current_date = current_datetime.date()
    return render_template('AppointmentViewer.html', appointments=booked_appointments)
    #if current_time == '9:00':
    #    c.execute('SELECT * FROM reminders WHERE remindertime = ?'(current_date))
    #    appointments.confirm_appointment()
    #    return render_template('AppointmentViewer.html', appointments=booked_appointments)
    #else:
    #    return render_template('AppointmentViewer.html', appointments=booked_appointments)


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
    booking_application.register_blueprint(appointments)
    init_db()  # initialize sqlite database
    return booking_application


if __name__ == '__main__':
    application = start_application()
    application.run(debug=True, host='0.0.0.0', port=5000)
