import sqlite3

conn = sqlite3.connect('appointments.db')
c = conn.cursor()

# Try to add the phone_no column
try:
    c.execute('ALTER TABLE appointments ADD COLUMN phone_no TEXT')
    print("✅ phone_no column added.")
except sqlite3.OperationalError as e:
    print("⚠️ Could not add column:", e)

conn.commit()
conn.close()