from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from models.db import query
from datetime import datetime, date

public = Blueprint('public', __name__)

@public.route('/')
def home():
    featured = query("SELECT * FROM menu_items WHERE is_featured=1 AND is_available=1 LIMIT 6")
    return render_template('index.html', featured=featured)

@public.route('/menu')
def menu():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    categories = ['Coffee','Tea','Cold Beverages','Pizza','Burgers','Sandwiches','Desserts']
    sql = "SELECT * FROM menu_items WHERE is_available=1"
    args = []
    if category and category in categories:
        sql += " AND category=%s"
        args.append(category)
    if search:
        sql += " AND (name LIKE %s OR description LIKE %s)"
        args.extend([f'%{search}%', f'%{search}%'])
    sql += " ORDER BY category, name"
    items = query(sql, args)
    return render_template('menu.html', items=items, categories=categories, active_cat=category, search=search)

@public.route('/booking', methods=['GET','POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        phone = request.form.get('phone','').strip()
        email = request.form.get('email','').strip()
        guests = request.form.get('guests', 1)
        bdate = request.form.get('date','')
        btime = request.form.get('time','')
        special = request.form.get('special_request','').strip()
        if not all([name, phone, email, bdate, btime]):
            flash('Please fill all required fields.', 'danger')
            return render_template('booking.html')
        # Check availability
        existing = query(
            "SELECT id FROM reservations WHERE date=%s AND time=%s AND status!='cancelled'",
            (bdate, btime), one=True
        )
        if existing:
            flash('Sorry, that time slot is already booked. Please choose another.', 'warning')
            return render_template('booking.html')
        query(
            "INSERT INTO reservations (name,phone,email,guests,date,time,special_request) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, phone, email, guests, bdate, btime, special), commit=True
        )
        flash('Reservation confirmed! We look forward to seeing you.', 'success')
        return redirect(url_for('public.booking'))
    return render_template('booking.html')

@public.route('/about')
def about():
    return render_template('about.html')

@public.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        subject = request.form.get('subject','').strip()
        message = request.form.get('message','').strip()
        if not all([name, email, message]):
            flash('Please fill all required fields.', 'danger')
            return render_template('contact.html')
        query(
            "INSERT INTO contacts (name,email,subject,message) VALUES (%s,%s,%s,%s)",
            (name, email, subject, message), commit=True
        )
        flash('Message sent! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('contact.html')

@public.route('/api/check-availability')
def check_availability():
    bdate = request.args.get('date')
    btime = request.args.get('time')
    if not bdate or not btime:
        return jsonify({'available': False, 'message': 'Missing date or time'})
    existing = query(
        "SELECT id FROM reservations WHERE date=%s AND time=%s AND status!='cancelled'",
        (bdate, btime), one=True
    )
    return jsonify({'available': not bool(existing)})
