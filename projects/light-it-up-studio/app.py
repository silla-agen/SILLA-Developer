from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database + table
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            service TEXT,
            date TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Booking Form Submit
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    service = request.form['service']
    date = request.form['date']
    message = request.form['message']

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO bookings (name, email, service, date, message)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, service, date, message))

    conn.commit()
    conn.close()

    return redirect('/')

# Admin Dashboard
@app.route('/admin')
def admin():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c.execute("SELECT * FROM bookings ORDER BY id DESC")
    bookings = c.fetchall()

    conn.close()

    return render_template('admin.html', bookings=bookings)

# Run App
if __name__ == '__main__':
    if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
