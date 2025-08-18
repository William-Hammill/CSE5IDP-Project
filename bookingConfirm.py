from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from Classes import Appointment, Pet, Service, database, reminderMessage
from datetime import datetime, timedelta
from Messaging import send_message, receive_message

appointments = Blueprint('appointments', __name__)


@appointments.route('/appointments/create/<int:id>', methods=['GET', 'POST'])
def create_appointment(appointment_id):
    pets = Pet.query_all()
    # services = Service.query.all()
    pets.name = request.form.get('pet_name')
    time_string = request.form.get('appointment_time').strip()
    date_string = request.form.get('appointment_date')
    appointment_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(time_string, '%I:%M %p').strftime('%H:%M')
    service_id = request.form.get('Service')
    assigned_employee = 'N/A'
    customer_first_name = request.form.get('customer_first_name')
    customer_last_name = request.form.get('customer_last_name')
    new_appointment = Appointment(pet_name=pets.name, customer_first_name=customer_first_name, client_last_name=customer_last_name, appointment_date=appointment_date,
                                  appointment_time=appointment_time,
                                  service_id=service_id, assigned_employee=assigned_employee, status='canceled')
    # reminder_time = appointment_time
    date_notice = timedelta(days=1)
    reminder_date = appointment_date - date_notice  # placeholder for determining 24 hour notification
    new_message = reminderMessage(client_name=new_appointment.customer_first_name, client_number=new_appointment.customer_number,
                                  pet_name=new_appointment.pet_name, appointment_date=new_appointment.appointment_date,
                                  appointment_time=new_appointment.appointment_time, reminder_date=reminder_date)
    database.session.add(new_appointment)
    database.session.add(new_message)
    database.session.commit()


@appointments.route('/appointments/reminder/<int:id>', methods=['GET', 'POST'])
def confirm_appointment(appointment_id):
    appointments = Appointment.query.get_or_404(appointment_id)
    messages = reminderMessage.query_all(appointment_id)
    contact_num = '(03) 5442 8880'
    current_timedate = datetime.now()
    current_time = current_timedate.time()
    currentdate = current_timedate.date()
    message = f'Hello {messages.client_name}, This is a reminder of your appointment at K9-Deli for {messages.pet_name} scheduled for {messages.appointment_date} at {messages.appointment_time}. Reply with Y to confirm your appointment or N to cancel. if you need to reschedule please ring {contact_num} '
    if current_time == '09:00' & currentdate == messages.reminder_date:
        send_message(message, appointments.client_number)
    message_response = receive_message()
    if message_response == 'Y':
        appointments.status = 'confirmed'
        database.session.commit()
    else:
        database.session.remove(appointments)
        # appointments.status = 'canceled'
        database.session.commit()


# def allocate_employee():
#    employee = Employee.query.all()
#    selected_appointment = Appointment.query.get_or_404()
#    selected_appointment.assigned_employee = employee
#    database.session.commit()
#    pass


def cancel_appointment():
    selected_appointment = Appointment.query.get_or_404()
    selected_appointment.status = 'canceled'
    database.session.commit()
    pass
