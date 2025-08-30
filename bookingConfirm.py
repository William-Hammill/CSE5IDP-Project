from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from Messaging import send_message, receive_message, send_placeholder, recieve_placeholder
import sqlite3

appointments = Blueprint('appointments', __name__)


@appointments.route('/appointments')
def load_page():
    return render_template('BookingLayout.html')


@appointments.route('/appointments/view')
def view_appointments():  # SQLITE version from simple_form branch
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    booked_appointments = c.fetchall()
    conn.close()
    return render_template('AppointmentViewer.html', appointments=booked_appointments)


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
    date_notice = timedelta(days=1)  # code to determine date for sending reminder/confirmation messages
    reminder_date = appointment_date - date_notice  # sets reminder send-date to day before appointment booking
    send_date = datetime.strftime(reminder_date, '%Y-%m-%d')
    c = conn.cursor()
    c.execute('''
               INSERT INTO appointments (customer_first, customer_last, appt_time, appt_date, pet_name, comments, appt_status)
               VALUES (?, ?, ?, ?, ?, ?, ?)
           ''', (
        customer_first_name, customer_last_name, appointment_time, appt_date, pets_name, comments,
        appointment_status))
    print('Successfully added appointment')
    c.execute('SELECT id from appointments')
    appointment_id = c.fetchone()
    appointment_reminder_id = [int(_) for _ in appointment_id]
    c.execute('''INSERT INTO reminders (customer_first, customer_last, customer_number, appt_time, 
    appt_date, pet_name, reminder_date, appointment_id) VALUES (?,?,?,?,?,?,?,?)''',
              (customer_first_name, customer_last_name, customer_number, appointment_time, appt_date, pets_name,
               send_date, appointment_reminder_id[0]))
    conn.commit()
    print('Successfully added reminder')
    conn.close()
    return redirect(url_for('appointments.view_appointments'))


@appointments.route('/confirm_appointment/<int:id>', methods=['GET', 'POST'])
def confirm_appointment(appointment_id):
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    contact_num = '(03) 5442 8880'
    current_timedate = datetime.now()
    current_time = current_timedate.time()
    current_date = current_timedate.date()
    if current_time == '09:00':  # & current_date == messages.reminder_date:
        c.execute('''SELECT reminder_date, customer_first_name, customer_number, pets_name, appointment_date, 
            appointment_time FROM reminders WHERE reminder_date = ? AND appointment_id = ?''', (current_date, appointment_id))
        messages = c.fetchall()
        message = f'Hello {messages[1]}, This is a reminder of your appointment at K9-Deli for {messages[3]} scheduled for {messages[4]} at {messages[5]}. Reply with Y to confirm your appointment or N to cancel. if you need to reschedule please ring {contact_num} '
        send_placeholder(message, messages[2])
        # send_message(message, appointment.customer_number)
        message_response = recieve_placeholder()
        if message_response == 'Y':
            c.execute('''
                    UPDATE appointments 
                    SET appt_status = 2
                    WHERE id = ?
                ''', (appointment_id,))
            conn.commit()
            conn.close()
            thanks_message = 'Thank you for confirming your appointment with us'
            send_placeholder(thanks_message, messages.customer_number)
        elif message_response == 'N' or message_response is None:
            cancel_appointment(appointment_id)
        # c.execute('''
        #             UPDATE appointments
        #             SET appt_status = 0
        #             WHERE id = ?
        #         ''', (appointment_id,))
        # conn.commit()
        # conn.close()


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
    c.execute('''
            UPDATE appointments 
            SET appt_status = 0
            WHERE id = ?
        ''', (appointment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('appointments.view_appointments'))
