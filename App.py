from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = 'reservations.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def execute_query(query, args=()):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

def fetch_query(query, args=(), one=False):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchone() if one else cur.fetchall()
    conn.close()
    return result
    
def get_all_reservations():
    query = "SELECT * FROM reservations"
    return fetch_query(query)

def total_sales():
    query = "SELECT COUNT(*) FROM reservations"
    return fetch_query(query, one=True)[0]

def is_admin_logged_in():
    return session.get('admin_logged_in', False)

def login_admin(password):
    if password == "admin_password":
        session['admin_logged_in'] = True
        return True
    return False

def logout_admin():
    session.pop('admin_logged_in', None)

@app.route('/')
def index():
    reservations = get_all_reservations()
    return render_template('index.html', reservations=reservations)

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        seat_row = request.form['seat_row']
        seat_column = request.form['seat_column']
        e_ticket_number = request.form['e_ticket_number']
        execute_query("INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES (?, ?, ?, ?)",
                      (passenger_name, seat_row, seat_column, e_ticket_number))
        return redirect(url_for('index'))
    return render_template('reserve.html')

@app.route('/cancel/<int:reservation_id>')
def cancel(reservation_id):
    execute_query("DELETE FROM reservations WHERE id=?", (reservation_id,))
    return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if login_admin(password):
            return redirect(url_for('admin_portal'))
        else:
            return render_template('admin_login.html', error="Invalid password")
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    logout_admin()
    return redirect(url_for('admin_login'))

@app.route('/admin/portal')
def admin_portal():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    reservations = get_all_reservations()
    total_sales_count = total_sales()
    return render_template('admin_portal.html', reservations=reservations, total_sales_count=total_sales_count)

if __name__ == '__main__':
    app.run(debug=True)
