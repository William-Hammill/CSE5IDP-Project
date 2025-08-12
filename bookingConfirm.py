from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from Classes import Appointment, Pet, Service, Employee, database, reminderMessage
from datetime import datetime
from Messaging import send_message, receive_message

appointments = Blueprint('appointments', __name__)
stored_appointments = []


def create_appointment():
    pets = Pet.query_all()
    services = Service.query.all()
    pets.id = request.form.get('pet_id')
    time_string = request.form.get('pet_id')
    date_string = request.form.get('pet_id')
    appointment_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(time_string, '%I:%M %p').strftime('%H:%M')
    service_id = request.form.get('Service')
    assigned_employee = 'N/A'
    contact_num = ''
    new_appointment = Appointment(pet_id=pets.id, appointment_date=appointment_date, appointment_time=appointment_time,
                                  service_id=service_id, assigned_employee=assigned_employee, status='unknown')
    new_message = reminderMessage(client_name=new_appointment.client_name, client_number=new_appointment.client_number,
                                  pet_name=new_appointment.pet, appointment_date=new_appointment.appointment_date,
                                  appointment_time=new_appointment.appointment_time)
    message = f'Hello {new_message.client_name} this message is to confirm your appointment at {new_message.appointment_time} on {new_message.appointment_date}. To confirm your appointment please respond with Y or yes, to cancel, send No or N, to reschedule your appointment please call us at {contact_num}'
    print("Do you want an automatic notification")
    new_message = reminderMessage(message)
    database.session.add(new_appointment)
    database.session.add(new_message)
    database.session.commit()
    # send_message(message, contact_num)
    # text_response = ''
    # confirm_appointment(text_response, new_appointment)


def confirm_appointment(appointment,):
    appointments = Appointment.query_all()
    messages = reminderMessage.query_all()
    contact_num = ''
    current_timedate = datetime.now()
    current_time = current_timedate.time()
    currentdate = current_timedate.date()
    message = f'Hello {messages.client_name} this message is to confirm your appointment at {messages.appointment_time} on {messages.appointment_date}. To confirm your appointment please respond with Y or yes, to cancel, send No or N, to reschedule your appointment please call us at {contact_num} '
    if current_time == messages.reminder_time & currentdate == messages.reminder_date:
        send_message(message, contact_num)
    message_response = receive_message()
    if message_response == 'Yes':
        appointment.status = 'confirmed'
        database.session.add(appointment)
        # database.session.remove(appointment)
        database.session.commit()
    else:
        appointment.status = 'canceled'
        database.session.add(appointment)
        # database.session.remove(appointment)
        database.session.commit()


def allocate_employee():
    employee = Employee.query.all()
    selected_appointment = Appointment.query.get_or_404()
    selected_appointment.assigned_employee = employee
    database.session.commit()
    pass


def cancel_appointment():
    selected_appointment = Appointment.query.get_or_404()
    selected_appointment.status = 'canceled'
    database.session.commit()
    pass
