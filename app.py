from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

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
            appt_datetime TEXT,
            pet_name TEXT,
            comments TEXT,
            phone_no TEXT,
            appt_status INTEGER DEFAULT 1 -- 1 Scheduled, 0 Cancelled, 2 Done
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Route to show the form
@app.route('/')
def home():
    return render_template('appointment_form.html', form_data={}, error=None)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':
        first_name = request.form['customer_first']
        last_name = request.form['customer_last']
        appt_time = request.form['appt_time']
        appt_date = request.form['appt_date']
        pet_name = request.form['pet_name']
        comments = request.form['comments']
        phone_no = request.form['phone_no']
        # Create a datetime object
        appt_datetime = datetime.strptime(f"{appt_date} {appt_time}", "%Y-%m-%d %H:%M")
        # Check for existing appointments
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        # Checks: appt_datetime + appt_status 1 (Scheduled). If these are both taken/true, then deny appointments for this time. 
        c.execute('SELECT * FROM appointments WHERE appt_datetime = ? AND appt_status = 1', (appt_datetime,))
        existing_appointments = c.fetchall()
        conn.close()
        if existing_appointments:
            error = "This appointment time is already booked. Please select another time."
            return render_template('appointment_form.html', error=error, form_data=request.form), 400
        # Insert data into SQLite
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO appointments (customer_first, customer_last, appt_datetime, pet_name, comments, phone_no, appt_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, appt_datetime, pet_name, comments, phone_no, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('view_appointments_latest'))


# Route to view latest/just-booked appointment
@app.route('/appointments_latest')
def view_appointments_latest():
    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()
    c.execute('SELECT customer_first, customer_last, pet_name, appt_datetime, phone_no, comments FROM appointments ORDER BY id DESC LIMIT 1')
    appointments = c.fetchall()
    conn.close()
    return render_template('appointment_latest_customer.html', appointments=appointments)

# Route to view appointments
@app.route('/appointments')
def view_appointments():
    # Current time so the db can refresh its appt_status' 
    # and mark past appointments as 'Done'
    current_time = datetime.now()

    conn = sqlite3.connect('appointments.db')
    conn.row_factory = sqlite3.Row # Enable dictionary-like row access in appointments_list.html
    c = conn.cursor()

    c.execute(''' 
        UPDATE appointments SET appt_status = 2 -- 2 = Done
        WHERE appt_datetime < ? AND appt_status = 1
    ''', (current_time,))
    conn.commit()

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
