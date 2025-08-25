from flask import Blueprint, render_template, request, redirect, url_for
# from Classes import Appointment, Pet, database, reminderMessage
from datetime import datetime, timedelta
from Messaging import send_message, receive_message, send_placeholder, recieve_placeholder
import sqlite3

appointments = Blueprint('appointments', __name__)
conn = sqlite3.connect('appointments.db')


@appointments.route('/appointments')
def view_appointments():  # SQLITE version from simple_form branch
    # conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    booked_appointments = c.fetchall()
    conn.close()
    return render_template('AppointmentViewer.html', appointments=booked_appointments)


@appointments.route('/create_appointment', methods=['POST'])
def create_appointment():
    # conn = sqlite3.connect('appointments.db')
    # pets = Pet.query_all()
    pets_name = request.form['pet_name']
    time_string = request.form['appointment_time'].strip()
    date_string = request.form['appointment_date']
    appointment_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(time_string, '%I:%M %p').strftime('%H:%M')
    customer_number = request.form['customer_number']
    customer_first_name = request.form['customer_first_name']
    customer_last_name = request.form['customer_last_name']
    comments = request.form['comments']
    appointment_status = 1  # 1 = scheduled, 0 = canceled, 2 = confirmed
    # new_appointment = Appointment(pet_name=pets.name, customer_first_name=customer_first_name,
    #                               client_last_name=customer_last_name,
    #                               appointment_date=appointment_date,
    #                               appointment_time=appointment_time,
    #                               assigned_employee=assigned_employee,
    #                               status='unknown')
    date_notice = timedelta(days=1)  # code to determine date for sending reminder/confirmation messages
    reminder_date = appointment_date - date_notice  # sets reminder send-date to day before appointment booking
    # new_message = reminderMessage(client_name=new_appointment.customer_first_name,
    #                               client_number=new_appointment.customer_number,
    #                               pet_name=new_appointment.pet_name,
    #                               appointment_date=new_appointment.appointment_date,
    #                               appointment_time=new_appointment.appointment_time,
    #                               reminder_date=reminder_date)
    # database.session.add(new_appointment)
    # database.session.add(new_message)
    # database.session.commit()
    c = conn.cursor()
    c.execute('''
               INSERT INTO appointments (customer_first, customer_last, appt_time, appt_date, pet_name, comments, appt_status)
               VALUES (?, ?, ?, ?, ?, ?, ?)
           ''', (
        customer_first_name, customer_last_name, appointment_time, appointment_date, pets_name, comments, appointment_status))
    c.execute('SELECT id from appointments')
    appointment_id = c.fetchall()
    c.execute('''INSERT INTO reminders (customer_first_name, customer_last_name, customer_number, appointment_time, 
    appointment_date, pets_name, reminder_date, appointment_id) VALUES (?,?,?,?,?,?,?,?)''',
              (customer_first_name, customer_last_name, customer_number, appointment_time, appointment_date, pets_name, reminder_date, appointment_id))
    conn.commit()
    conn.close()
    return url_for('AppointmentViewer')


@appointments.route('/confirm_appointment/<int:id>', methods=['GET', 'POST'])
def confirm_appointment(appointment_id):
    # conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    # appointment = Appointment.query.get_or_404(appointment_id)
    # messages = reminderMessage.query_all(appointment_id)
    contact_num = '(03) 5442 8880'
    current_timedate = datetime.now()
    current_time = current_timedate.time()
    current_date = current_timedate.date()
    c.execute('''SELECT reminder_date, customer_first_name, customer_number, pets_name, appointment_date, 
    appointment_time FROM reminders WHERE reminder_date = ?''', (current_date,))
    messages = c.fetchall()
    message = f'Hello {messages.customer_first_name}, This is a reminder of your appointment at K9-Deli for {messages.pet_name} scheduled for {messages.appointment_date} at {messages.appointment_time}. Reply with Y to confirm your appointment or N to cancel. if you need to reschedule please ring {contact_num} '
    if current_time == '09:00' & current_date == messages.reminder_date:
        send_placeholder(message, messages.customer_number)
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
        # appointment.status = 'confirmed'
        # database.session.commit()
    elif message_response == 'N' or message_response is None:
        # database.session.remove(appointments)
        c.execute('''
                    UPDATE appointments 
                    SET appt_status = 0
                    WHERE id = ?
                ''', (appointment_id,))
        conn.commit()
        conn.close()
        # appointment.status = 'canceled'
    # database.session.commit()


# @appointments.route('/appointments/view', methods=['POST'])
# def view_appointments():  # SQLAcademy version
# pets = Pet.query_all()
# today = datetime.now().date()
# upcoming_appointments = Appointment.query.filter(
#    Appointment.date > today,
#    Appointment.status != 'canceled'
# ).join(Pet).all()

# return render_template('AppointmentViewer.html',upcoming_appointments=upcoming_appointments,pets=pets)
# return (url_for('AppointmentViewer'))


#def allocate_employee(appointment_id, employee_id):
    #conn = sqlite3.connect('appointments.db')
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
    # selected_appointment = Appointment.query.get_or_404()
    # selected_appointment.status = 'canceled'
    # database.session.commit()
  #  conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
            UPDATE appointments 
            SET appt_status = 0
            WHERE id = ?
        ''', (appointment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_appointments'))
