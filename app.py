from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# SQLite database setup (ensure the database exists)
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
            phone_no TEXT,
            appt_status INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to show the form
@app.route('/')
def home():
    return render_template('appointment_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':
        first_name = request.form['customer_first']
        last_name = request.form['customer_last']
        appt_time = request.form['appt_time']
        appt_date = request.form['appt_date']
        pet_name = request.form['pet_name']
        phone_no = request.form['phone_no']
        comments = request.form['comments']
        appt_status = 1  # Default: Scheduled

        # Insert data into SQLite
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO appointments (customer_first, customer_last, appt_time, appt_date, pet_name, phone_no, comments, appt_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, appt_time, appt_date, pet_name, phone_no, comments, appt_status))
        conn.commit()
        conn.close()

        return redirect(url_for('view_appointments_latest'))

# Route to view latest/just-booked appointment
@app.route('/appointments_latest')
def view_appointments_latest():
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row# Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT customer_first, customer_last, pet_name, appt_time, appt_date, phone_no, comments FROM appointments ORDER BY id DESC LIMIT 1')
    appointments = c.fetchall()
    conn.close()
    return render_template('appointment_latest_customer.html', appointments=appointments)

# Route to view appointments
@app.route('/appointments')
def view_appointments():
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row# Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    appointments = c.fetchall()
    conn.close()
    return render_template('appointments_list.html', appointments=appointments)

# Route to cancel an appointment
@app.route('/cancel/<int:appointment_id>')
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

    return redirect(url_for('view_appointments'))

if __name__ == '__main__':
    app.run(debug=True)
