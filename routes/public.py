from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models.db import query

public = Blueprint('public', __name__)


@public.route('/')
def home():

    try:

        featured = query(
            """
            SELECT * FROM menu_items
            WHERE is_featured=1
            AND is_available=1
            LIMIT 6
            """
        )

    except Exception as e:

        print("HOME ERROR:", str(e))

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

    try:

        category = request.args.get('category', '')
        search = request.args.get('search', '')

        sql = """
        SELECT * FROM menu_items
        WHERE is_available=1
        """

        args = []

        if category and category in categories:

            sql += " AND category=%s"

            args.append(category)

        if search:

            sql += """
            AND (
                name LIKE %s
                OR description LIKE %s
            )
            """

            args.extend([
                f'%{search}%',
                f'%{search}%'
            ])

        sql += " ORDER BY category, name"

        items = query(sql, args)

    except Exception as e:

        print("MENU ERROR:", str(e))

        items = []

    return render_template(
        'menu.html',
        items=items,
        categories=categories,
        active_cat=category if 'category' in locals() else '',
        search=search if 'search' in locals() else ''
    )


@public.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        try:

            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            guests = request.form.get('guests', 1)
            bdate = request.form.get('date', '')
            btime = request.form.get('time', '')
            special = request.form.get(
                'special_request',
                ''
            ).strip()

            if not all([name, phone, email, bdate, btime]):

                flash(
                    'Please fill all required fields.',
                    'danger'
                )

                return render_template('booking.html')

            existing = query(
                """
                SELECT id FROM reservations
                WHERE date=%s
                AND time=%s
                AND status!='cancelled'
                """,
                (bdate, btime),
                one=True
            )

            if existing:

                flash(
                    'Sorry, that time slot is already booked.',
                    'warning'
                )

                return render_template('booking.html')

            query(
                """
                INSERT INTO reservations
                (
                    name,
                    phone,
                    email,
                    guests,
                    date,
                    time,
                    special_request
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    name,
                    phone,
                    email,
                    guests,
                    bdate,
                    btime,
                    special
                ),
                commit=True
            )

            flash(
                'Reservation confirmed!',
                'success'
            )

            return redirect(
                url_for('public.booking')
            )

        except Exception as e:

            print("BOOKING ERROR:", str(e))

            flash(
                'Something went wrong.',
                'danger'
            )

    return render_template('booking.html')


@public.route('/about')
def about():

    return render_template('about.html')


@public.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        try:

            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()

            if not all([name, email, message]):

                flash(
                    'Please fill all required fields.',
                    'danger'
                )

                return render_template('contact.html')

            query(
                """
                INSERT INTO contacts
                (name,email,subject,message)
                VALUES (%s,%s,%s,%s)
                """,
                (
                    name,
                    email,
                    subject,
                    message
                ),
                commit=True
            )

            flash(
                'Message sent!',
                'success'
            )

            return redirect(
                url_for('public.contact')
            )

        except Exception as e:

            print("CONTACT ERROR:", str(e))

            flash(
                'Something went wrong.',
                'danger'
            )

    return render_template('contact.html')


@public.route('/api/check-availability')
def check_availability():

    try:

        bdate = request.args.get('date')
        btime = request.args.get('time')

        if not bdate or not btime:

            return jsonify({
                'available': False,
                'message': 'Missing date or time'
            })

        existing = query(
            """
            SELECT id FROM reservations
            WHERE date=%s
            AND time=%s
            AND status!='cancelled'
            """,
            (bdate, btime),
            one=True
        )

        return jsonify({
            'available': not bool(existing)
        })

    except Exception as e:

        print(
            "AVAILABILITY ERROR:",
            str(e)
        )

        return jsonify({
            'available': False
        })