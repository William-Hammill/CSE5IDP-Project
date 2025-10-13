from flask import Flask, render_template
from datetime import datetime
from bookingConfirm import appointments, confirm_auto, confirm_appointment
import sqlite3
import time
import threading

booking_application = Flask(__name__)
stop_thread = threading.Event()


@booking_application.route('/')
def home():
    return render_template('WelcomePage.html')


def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_first TEXT,
                customer_last TEXT,
                customer_number TEXT,
                appt_datetime TEXT,
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
                    customer_number TEXT,
                    appt_time TEXT,
                    appt_date TEXT,
                    pet_name TEXT,
                    reminder_date TEXT,
                    appointment_id INTEGER,
                    FOREIGN KEY(appointment_id) REFERENCES appointments(id)
                )
            ''')
    c.execute('''
                    CREATE TABLE IF NOT EXISTS Sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        appt_datetime TEXT,
                        session_limit INTEGER
                    )
                ''')
    conn.commit()
    conn.close()


def start_application():
    booking_application.register_blueprint(appointments)
    init_db()  # initialize sqlite database
    # current_datetime = datetime.now()
    # current_time = current_datetime.time()
    # time = current_time.strftime('%H:%M')
    # print(time)
    # if time == '13:29':
    #    send_reminders()  # Send appointment reminders automatically
    # schedule.every().day.at('09:00').do(send_reminders)
    return booking_application


def send_reminders():
    current_datetime = datetime.now()
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    current_date = current_datetime.date()
    c.execute('''SELECT appointment_id FROM reminders WHERE reminder_date = ? ORDER BY appt_time DESC''',
              (current_date,))
    reminder_messages = c.fetchall()
    if reminder_messages is None:
        print('No appointments available')
        return
    for reminder in reminder_messages:
        appointment_reminder_id = int(reminder[0])
        c.execute('''SELECT appt_status FROM appointments WHERE id = ?''', (appointment_reminder_id,))
        status = c.fetchone()
        appt_status = int(status[0])
        if appt_status == 1:
            confirm_auto(appointment_reminder_id)
            print('reminders sent')
    conn.close()
    return


def message_loop(event):
    while not event.is_set():
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        reminder_time = current_time.strftime('%H:%M')
        if reminder_time == '09:00':
            print('Sending reminders')
            send_reminders()
            time.sleep(60)


if __name__ == '__main__':
    application = start_application()
    loop_thread = threading.Thread(target=message_loop, args=(stop_thread,))
    loop_thread.daemon = True
    print('starting message loop')
    loop_thread.start()
    application.run(debug=True, host='0.0.0.0', port=5000)
    stop_thread.set()
    print('stopping message loop')
