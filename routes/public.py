from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

public = Blueprint('public', __name__)


@public.route('/')
def home():

    # TEMPORARY FIX
    # DB query disabled because Render loading issue

    featured = []

    return render_template(
        'index.html',
        featured=featured
    )


@public.route('/menu')
def menu():

    categories = [
        'Coffee',
        'Tea',
        'Cold Beverages',
        'Pizza',
        'Burgers',
        'Sandwiches',
        'Desserts'
    ]

    # TEMPORARY STATIC DATA

    items = [
        {
            "name": "Cappuccino",
            "description": "Rich coffee with milk foam",
            "price": 180,
            "image": "cafe1.jpg",
            "category": "Coffee"
        },
        {
            "name": "Cold Coffee",
            "description": "Chilled creamy coffee",
            "price": 220,
            "image": "cafe2.jpg",
            "category": "Cold Beverages"
        }
    ]

    return render_template(
        'menu.html',
        items=items,
        categories=categories,
        active_cat='',
        search=''
    )


@public.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        flash(
            'Booking feature temporarily disabled.',
            'warning'
        )

        return redirect(
            url_for('public.booking')
        )

    return render_template('booking.html')


@public.route('/about')
def about():

    return render_template('about.html')


@public.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        flash(
            'Message sent successfully!',
            'success'
        )

        return redirect(
            url_for('public.contact')
        )

    return render_template('contact.html')


@public.route('/api/check-availability')
def check_availability():

    return jsonify({
        'available': True
    })