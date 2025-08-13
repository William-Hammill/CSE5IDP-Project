from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Appointment(database.model):
    id = database.Column(database.Integer, primary_key=True)
    time = database.Column(database.String(5),nullable=False)
    date = database.Column(database.Date,nullable=False)
    client_number = database.Column(database.Integer(50),nullable=False)
    client_name = database.Column(database.String(50),nullable=False)
    status = database.Column(database.String(20),nullable=False)  # 3 possible values: confirmed, canceled or unknown
    pet_id = database.Column(database.Integer, database.ForeignKey('pet.id'), nullable=False)
    pet = database.relationship('Pet', back_populates='appointments')
    assigned_employee = database.relationship('Employee', back_populates='appointments')

    #service_id = database.Column(database.Integer, database.ForeignKey('service.id'))
    #servicetype = database.relationship('Service', back_populates='appointments')

    @staticmethod
    def add(pet_id, date, time, service_id, status='unknown'):
        new_appointment = Appointment(
            pet_id=pet_id,
            date=date,
            time=time,
            service_id=service_id,
            status=status
        )
        database.session.add(new_appointment)
        database.session.commit()

    @staticmethod
    def get_appointments():
        return Appointment.query.all()


class Pet(database.model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100),nullable=False)
    owner = database.Column(database.String(100),nullable=False)

    appointments = database.relationship('Appointment', back_populates='pets', lazy=True)

    @staticmethod
    def add(pet_id, name, owner):
        new_pet = Pet(
            pet_id=pet_id,
            name=name,
            owner=owner
        )
        database.session.add(new_pet)
        database.session.commit()

    @staticmethod
    def get_pets():
        return Pet.query.all()


class Service(database.model):
    service_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.string(100))

    appointments = database.relationship('Appointment', back_populates='service', lazy=True)

    @staticmethod
    def add(service_id, name):
        new_service = Service(
            service_id=service_id,
            name=name,
        )
        database.session.add(new_service)
        database.session.commit()

    @staticmethod
    def get_services():
        return Service.query.all()


class Employee(database.model):
    employee_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50))

    appointments = database.relationship('Appointment', back_populates='pets', lazy=True)

    @staticmethod
    def add(employee_id, name):
        new_employee = Employee(
            employee_id=employee_id,
            name=name,
        )
        database.session.add(new_employee)
        database.session.commit()

    @staticmethod
    def get_employees():
        return Employee.query.all()

class reminderMessage(database.model):
    id = database.Column(database.Integer, primary_key=True)
    client_name = database.column(database.string(50),database.ForeignKey('appointment.client_name'),nullable=False)
    client_number = database.column(database.Integer(50),database.ForeignKey('appointment.client_number'),nullable=False)
    pet_name = database.column(database.string(50),database.ForeignKey('pet.pet_name'),nullable=False)
    appointment_time = database.Column(database.String(50),nullable=False)
    appointment_date = database.Column(database.Date,nullable=False)
    reminder_time = database.Column(database.String(50), nullable=False)
    reminder_date = database.Column(database.Date, nullable=False)
    appointment_id = database.Column(database.integer, database.ForeignKey('appointment.id'))

    appointments = database.relationship('Appointment', back_populates='', lazy=True)

    @staticmethod
    def add(id, client_name, client_number, pet_name, appointment_time, appointment_date, reminder_time, reminder_date):
        new_reminder = reminderMessage(
            id=id,
            client_name=client_name,
            client_number=client_number,
            pet_name=pet_name,
            appointment_time=appointment_time,
            appointment_date=appointment_date,
            reminder_time=reminder_time,
            reminder_date=reminder_date
        )
        database.session.add(new_reminder)
        database.session.commit()
    @staticmethod
    def get_reminders():
        return reminderMessage.query.all()