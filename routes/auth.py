from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.db import query
from functools import wraps

auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') not in ('admin','staff'):
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','')
        password = request.form.get('password','')
        user = query("SELECT * FROM users WHERE email=%s", (email,), one=True)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','')
        if not all([name, email, password]):
            flash('All fields required.', 'danger')
            return render_template('auth/register.html')
        existing = query("SELECT id FROM users WHERE email=%s", (email,), one=True)
        if existing:
            flash('Email already registered.', 'warning')
            return render_template('auth/register.html')
        hashed = generate_password_hash(password)
        query("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name,email,hashed), commit=True)
        flash('Registered successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
