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
