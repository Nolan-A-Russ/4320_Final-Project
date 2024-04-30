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
