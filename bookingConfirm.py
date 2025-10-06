from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from Messaging import send_message, receive_message
import sqlite3
from time import sleep

appointments = Blueprint('appointments', __name__)


# Loads appointment Booking page
@appointments.route('/appointments')
def load_page():
    return render_template('BookingLayout.html')


# Generates response for first time customers
@appointments.route('/appointments/questionnaire')
def load_questionnaire():
    return "Thank you for answering, Unfortunately online bookings are for repeat customers only. To make an " \
           "appointment please call us at (03) 5442 8880" + render_template('WelcomePage.html'), 400
    # return render_template('QuestionnairePage.html')


@appointments.route('/appointments/questionnaireAnswers', methods=['POST'])
def submit_questionnaire():
    # answer_1 = request.form['answer_1']
    # answer_2 = request.form['answer_2']
    # answer_3 = request.form['answer_3']
    # answer_4 = request.form['answer_4']
    # conn = sqlite3.connect('appointments.db')
    # c = conn.cursor()
    # c.execute('''INSERT INTO Questionnaires (answer_1, answer_2, answer_3, answer_4) VALUES (?, ?, ?, ?)''',
    #          (answer_1, answer_2, answer_3, answer_4))
    return "Thank you for answering, Unfortunately online bookings are for repeat customers only. To make an " \
           "appointment please call us at (03) 5442 8880, we apologize for the inconvenience", 400


# Updates appointment list based on status and time of day
@appointments.route('/appointments/view')
def view_appointments():  # SQLITE version from simple_form branch
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    current_time = datetime.now()
    c = conn.cursor()
    c.execute(''' 
            UPDATE appointments SET appt_status = 2 -- 2 = Done
            WHERE appt_datetime < ? AND appt_status = 1 OR appt_datetime < ? AND appt_status = 3
        ''', (current_time, current_time))
    c.execute('SELECT * FROM appointments')
    booked_appointments = c.fetchall()
    conn.close()
    return render_template('AppointmentViewer.html', appointments=booked_appointments)


# Adds appointments to database and generates reminder messages.
@appointments.route('/create_appointment', methods=['POST'])
def create_appointment():
    conn = sqlite3.connect('appointments.db')
    pets_name = request.form['pet_name']
    appointment_time = request.form['appt_time'].strip()
    appt_date = request.form['appt_date']
    appointment_date = datetime.strptime(appt_date, '%Y-%m-%d')
    # appointment_time = datetime.strptime(time_string, '%I:%M %p').strftime('%H:%M')
    customer_number = request.form['customer_number']
    customer_first_name = request.form['customer_first']
    customer_last_name = request.form['customer_last']
    comments = request.form['comments']
    appointment_status = 1  # 1 = scheduled, 0 = canceled, 2 = confirmed
    date_notice = timedelta(days=2)  # code to determine date for sending reminder/confirmation messages
    reminder_date = appointment_date - date_notice  # sets reminder send-date to day before appointment booking
    send_date = datetime.strftime(reminder_date, '%Y-%m-%d')
    appt_datetime = datetime.strptime(f"{appt_date} {appointment_time}", "%Y-%m-%d %H:%M")
    c = conn.cursor()
    c.execute('SELECT id FROM Sessions WHERE appt_datetime = ?', (appt_datetime,))
    session_id = c.fetchone()
    # print(session_id)
    # Check to see if session exists
    if session_id is None:
        session_limit = 0
        c.execute('''INSERT INTO Sessions (appt_datetime, session_limit) VALUES (?,?)''',
                  (str(appt_datetime), session_limit))
        print('Added session to database')
    # retrieves limit number from session
    c.execute('SELECT session_limit FROM Sessions WHERE appt_datetime = ?', (appt_datetime,))
    new_limit = c.fetchone()
    current_time = datetime.now()
    # checks to see if session has any free slots
    if int(new_limit[0]) == 8:
        return "This Session is fully booked. Please select another time." + render_template('BookingLayout.html'), 400
    # checks to see if selected time is before current time
    if appt_datetime < current_time:
        return "This timeslot has already passed. Please select another time." + render_template('BookingLayout.html'), 400
    c.execute('''INSERT INTO appointments (customer_first, customer_last, customer_number, appt_datetime, pet_name, 
    comments, appt_status) VALUES (?, ?, ?, ?, ?, ?, ?) ''', (customer_first_name, customer_last_name,
                                                              customer_number, appt_datetime, pets_name, comments,
                                                              appointment_status))

    # update session limit
    limit = int(new_limit[0])
    session_number = limit + 1
    print(session_number)
    c.execute('''UPDATE Sessions SET session_limit = ? WHERE appt_datetime = ? ''',
              (session_number, str(appt_datetime),))
    print('Successfully added appointment')
    # print(customer_number)
    # retrieve id from newly made appointment to add to reminder message
    c.execute('SELECT id from appointments ORDER BY id DESC')
    appointment_id = c.fetchone()
    appointment_reminder_id = int(appointment_id[0])  # [int(_) for _ in appointment_id]
    # print(appointment_reminder_id)
    c.execute('''INSERT INTO reminders (customer_first, customer_last, customer_number, appt_time, 
                appt_date, pet_name, reminder_date, appointment_id) VALUES (?,?,?,?,?,?,?,?)''',
              (customer_first_name, customer_last_name, customer_number, appointment_time, appt_date, pets_name,
               send_date, appointment_reminder_id))
    conn.commit()
    print('Successfully added reminder')
    conn.close()
    return redirect(url_for('appointments.view_appointments'))


@appointments.route('/confirm_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def confirm_appointment(appointment_id):
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    contact_num = '(03) 5442 8880'
    current_timedate = datetime.now()
    current_date = current_timedate.date()
    # retrieve date and time for reminders (48 hours prior to appointment time)
    c.execute('''SELECT customer_first, customer_number, pet_name, appt_date, 
                appt_time FROM reminders WHERE reminder_date = ? AND appointment_id = ?''',
              (current_date, appointment_id))
    messages = c.fetchone()
    # print(messages[2])
    message = f'Hello {messages[0]}, This is a reminder of your appointment at K9-Deli for {messages[2]} scheduled for {messages[3]} at {messages[4]}. Reply with Y to confirm your appointment or N to cancel. if you need to reschedule, please ring {contact_num} '
    # send above template using twilio client, See messaging.py for more info.
    send_message(message, messages[1])
    # wait for text message response
    sleep(15)
    # retrieve response via twilio client
    message_response = receive_message(messages[1])
    if message_response == 'Y' or message_response is None:
        c.execute('''
                    UPDATE appointments 
                    SET appt_status = 3
                    WHERE id = ?
                ''', (appointment_id,))
        conn.commit()
        conn.close()
        thanks_message = 'Thank you for confirming your appointment with us'
        send_message(thanks_message, messages[1])
        # send_placeholder(thanks_message, messages[1])
        #return "Please refresh to see appointment changes", 400
        return redirect(url_for('appointments.view_appointments'))
    elif message_response == 'N':
        cancel_appointment(appointment_id)
        #return "Please refresh to see appointment changes", 400
        return redirect(url_for('appointments.view_appointments'))


# placeholder function for allocating employees to appointments
# def allocate_employee(appointment_id, employee_id):
# conn = sqlite3.connect('appointments-old.db')
#   c = conn.cursor()
#  c.execute('''UPDATE appointments
#               SET appt_employee = ?
#               WHERE id = ?
#               ''', (appointment_id, employee_id))
#  conn.commit()
#  conn.close()
#  return redirect(url_for('AppointmentViewer'))

@appointments.route('/cancel/<int:appointment_id>')
def cancel_appointment(appointment_id):
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('SELECT appt_datetime FROM appointments WHERE id = ?', (appointment_id,))
    date = c.fetchone()
    sessiondate = str(date[0])
    print(sessiondate)
    c.execute('SELECT session_limit FROM Sessions WHERE appt_datetime = ?', (sessiondate,))
    limit = c.fetchone()
    print(limit)
    session_number = int(limit[0])
    new_limit = session_number - 1
    c.execute('''
                UPDATE Sessions 
                SET session_limit = ?
                WHERE appt_datetime = ?
            ''', (new_limit, sessiondate,))
    c.execute('''
            UPDATE appointments 
            SET appt_status = 0
            WHERE id = ?
        ''', (appointment_id,))
    conn.commit()
    conn.close()
    #return "Please refresh to see appointment changes"
    return redirect(url_for('appointments.view_appointments'))
