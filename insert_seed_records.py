import sqlite3

conn = sqlite3.connect('appointments.db')
c = conn.cursor()

try:
    c.execute("INSERT INTO appointments (customer_first, customer_last, appt_time, appt_date, pet_name, phone_no, comments, appt_status) VALUES ('New', 'Guy', '09:00', '	2025-08-26', 'Titus', '0465100200', 'This is a sample comment', 1);")
    c.execute("INSERT INTO appointments (customer_first, customer_last, appt_time, appt_date, pet_name, phone_no, comments, appt_status) VALUES ('John', 'Doe', '14:00', '2025-08-27', 'King Joe', '0467100200', 'Example comment', 1);")
    print("Sample records added.")
    # id_to_delete = 11
    # c.execute('DELETE FROM appointments WHERE id = ?', (id_to_delete,))
    # conn.commit()
    # print('Delete successful')
except sqlite3.OperationalError as e:
    print("ERROR: Could not del", e)

conn.commit()
conn.close()