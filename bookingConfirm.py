from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from Classes import Appointment, Pet, Service, database, reminderMessage
from datetime import datetime, timedelta
from Messaging import send_message, receive_message

appointments = Blueprint('appointments', __name__)


@appointments.route('/appointments/create/<int:id>', methods=['GET', 'POST'])
def create_appointment():
    pets = Pet.query_all()
    pets.name = request.form.get('pet_name')
    time_string = request.form.get('appointment_time').strip()
    date_string = request.form.get('appointment_date')
    appointment_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(time_string, '%I:%M %p').strftime('%H:%M')
    assigned_employee = 'N/A'
    customer_first_name = request.form.get('customer_first_name')
    customer_last_name = request.form.get('customer_last_name')
    new_appointment = Appointment(pet_name=pets.name, customer_first_name=customer_first_name,
                                  client_last_name=customer_last_name,
                                  appointment_date=appointment_date,
                                  appointment_time=appointment_time,
                                  assigned_employee=assigned_employee,
                                  status='unknown')
    date_notice = timedelta(days=1)  # code to determine date for sending reminder/confirmation messages
    reminder_date = appointment_date - date_notice
    new_message = reminderMessage(client_name=new_appointment.customer_first_name,
                                  client_number=new_appointment.customer_number,
                                  pet_name=new_appointment.pet_name,
                                  appointment_date=new_appointment.appointment_date,
                                  appointment_time=new_appointment.appointment_time,
                                  reminder_date=reminder_date)
    database.session.add(new_appointment)
    database.session.add(new_message)
    database.session.commit()


@appointments.route('/appointments/reminder/<int:id>', methods=['GET', 'POST'])
def confirm_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    messages = reminderMessage.query_all(appointment_id)
    contact_num = '(03) 5442 8880'
    current_timedate = datetime.now()
    current_time = current_timedate.time()
    current_date = current_timedate.date()
    message = f'Hello {messages.client_name}, This is a reminder of your appointment at K9-Deli for {messages.pet_name} scheduled for {messages.appointment_date} at {messages.appointment_time}. Reply with Y to confirm your appointment or N to cancel. if you need to reschedule please ring {contact_num} '
    if current_time == '09:00' & current_date == messages.reminder_date:
        send_message(message, appointment.client_number)
    message_response = receive_message()
    if message_response == 'Y':
        appointment.status = 'confirmed'
        database.session.commit()
    elif message_response == 'N' or message_response is None:
        # database.session.remove(appointments)
        appointment.status = 'canceled'
        database.session.commit()


@appointments.route('/appointments/view', methods=['POST'])
def view_appointments():
    pets = Pet.query_all()
    today = datetime.now().date()
    upcoming_appointments = Appointment.query.filter(
        Appointment.date > today,
        Appointment.status != 'canceled'
    ).join(Pet).all()

    return render_template('AppointmentViewer.html',
                           upcoming_appointments=upcoming_appointments,
                           pets=pets)


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
