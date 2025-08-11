from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, time

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Role can be 'employee', 'manager', or 'superuser'

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def create_superuser():
        if User.query.filter_by(username='superUser').first() is None:
            superuser = User(username='superUser', role='superuser')
            superuser.set_password('superpass')  # Password is hashed here
            db.session.add(superuser)
            db.session.commit()
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))
    
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_number = db.Column(db.String(15))

    appointments = db.relationship('Appointment', back_populates='pet', lazy=True)

    @staticmethod
    def add(pet_name, breed, owner_name, address, contact_number, email, emergency_contact_name=None, emergency_contact_number=None):
        new_pet = Pet(
            pet_name=pet_name,
            breed=breed,
            owner_name=owner_name,
            address=address,
            contact_number=contact_number,
            email=email,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number
        )
        db.session.add(new_pet)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pet.query.all()


# ServiceType model
from extensions import db

# ServiceType model
class ServiceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)  # service price
    is_visible = db.Column(db.Boolean,default=True) # show/hide service
    duration = db.Column(db.Integer, nullable=False)  # ervice duration in minutes

    appointments = db.relationship('Appointment', back_populates='service_type', lazy=True)

    @staticmethod
    def add(name, price, duration,is_visible):
        new_service = ServiceType(name=name, price=price, duration=duration, is_visible=is_visible)
        db.session.add(new_service)
        db.session.commit()

    @staticmethod
    def get_all():
        return ServiceType.query.all()

# Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(5))  # Format: HH:MM (24-hour format)
    comments = db.Column(db.String(200))
    
    # New status field to track appointment status
    status = db.Column(db.String(20), default='scheduled')  # Possible values: 'scheduled', 'canceled'

    # Foreign keys
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', back_populates='appointments')
    
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
    service_type = db.relationship('ServiceType', back_populates='appointments')

    @staticmethod
    def add(pet_id, date, time, service_type_id, comments='', status='scheduled'):
        new_appointment = Appointment(
            pet_id=pet_id, 
            date=date, 
            time=time, 
            service_type_id=service_type_id, 
            comments=comments, 
            status=status  # Set initial status
        )
        db.session.add(new_appointment)
        db.session.commit()

    @staticmethod
    def get_all():
        return Appointment.query.all()
