from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from routes.auth import admin_required
from models.db import query
from werkzeug.utils import secure_filename
import os, uuid

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED = {'png','jpg','jpeg','gif','webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED

def save_image(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.',1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return filename
    return None

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'menu_count': query("SELECT COUNT(*) as c FROM menu_items", one=True)['c'],
        'reservations': query("SELECT COUNT(*) as c FROM reservations", one=True)['c'],
        'pending': query("SELECT COUNT(*) as c FROM reservations WHERE status='pending'", one=True)['c'],
        'contacts': query("SELECT COUNT(*) as c FROM contacts WHERE is_read=0", one=True)['c'],
    }
    recent_reservations = query("SELECT * FROM reservations ORDER BY created_at DESC LIMIT 5")
    monthly_data = query("""
        SELECT MONTH(created_at) as month, COUNT(*) as count
        FROM reservations WHERE YEAR(created_at)=YEAR(NOW())
        GROUP BY MONTH(created_at)
    """)
    category_data = query("SELECT category, COUNT(*) as count FROM menu_items GROUP BY category")
    return render_template('admin/dashboard.html', stats=stats,
        recent_reservations=recent_reservations,
        monthly_data=monthly_data, category_data=category_data)

# --- Menu ---
@admin_bp.route('/menu')
@admin_required
def menu():
    items = query("SELECT * FROM menu_items ORDER BY category, name")
    return render_template('admin/menu.html', items=items)

@admin_bp.route('/menu/add', methods=['GET','POST'])
@admin_required
def menu_add():
    categories = ['Coffee','Tea','Cold Beverages','Pizza','Burgers','Sandwiches','Desserts']
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        desc = request.form.get('description','').strip()
        price = request.form.get('price', 0)
        cat = request.form.get('category','')
        featured = 1 if request.form.get('is_featured') else 0
        available = 1 if request.form.get('is_available') else 0
        image = 'default.jpg'
        if 'image' in request.files:
            saved = save_image(request.files['image'])
            if saved:
                image = saved
        query("INSERT INTO menu_items (name,description,price,category,image,is_featured,is_available) VALUES (%s,%s,%s,%s,%s,%s,%s)",
              (name,desc,price,cat,image,featured,available), commit=True)
        flash('Menu item added.', 'success')
        return redirect(url_for('admin.menu'))
    return render_template('admin/menu_form.html', item=None, categories=categories)

@admin_bp.route('/menu/edit/<int:id>', methods=['GET','POST'])
@admin_required
def menu_edit(id):
    categories = ['Coffee','Tea','Cold Beverages','Pizza','Burgers','Sandwiches','Desserts']
    item = query("SELECT * FROM menu_items WHERE id=%s", (id,), one=True)
    if not item:
        flash('Item not found.', 'danger')
        return redirect(url_for('admin.menu'))
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        desc = request.form.get('description','').strip()
        price = request.form.get('price', 0)
        cat = request.form.get('category','')
        featured = 1 if request.form.get('is_featured') else 0
        available = 1 if request.form.get('is_available') else 0
        image = item['image']
        if 'image' in request.files and request.files['image'].filename:
            saved = save_image(request.files['image'])
            if saved:
                image = saved
        query("UPDATE menu_items SET name=%s,description=%s,price=%s,category=%s,image=%s,is_featured=%s,is_available=%s WHERE id=%s",
              (name,desc,price,cat,image,featured,available,id), commit=True)
        flash('Menu item updated.', 'success')
        return redirect(url_for('admin.menu'))
    return render_template('admin/menu_form.html', item=item, categories=categories)

@admin_bp.route('/menu/delete/<int:id>', methods=['POST'])
@admin_required
def menu_delete(id):
    query("DELETE FROM menu_items WHERE id=%s", (id,), commit=True)
    flash('Item deleted.', 'success')
    return redirect(url_for('admin.menu'))

# --- Reservations ---
@admin_bp.route('/reservations')
@admin_required
def reservations():
    items = query("SELECT * FROM reservations ORDER BY date DESC, time DESC")
    return render_template('admin/reservations.html', items=items)

@admin_bp.route('/reservations/update/<int:id>', methods=['POST'])
@admin_required
def reservation_update(id):
    status = request.form.get('status')
    query("UPDATE reservations SET status=%s WHERE id=%s", (status, id), commit=True)
    flash('Reservation updated.', 'success')
    return redirect(url_for('admin.reservations'))

@admin_bp.route('/reservations/delete/<int:id>', methods=['POST'])
@admin_required
def reservation_delete(id):
    query("DELETE FROM reservations WHERE id=%s", (id,), commit=True)
    flash('Reservation deleted.', 'success')
    return redirect(url_for('admin.reservations'))

# --- Contacts ---
@admin_bp.route('/contacts')
@admin_required
def contacts():
    items = query("SELECT * FROM contacts ORDER BY created_at DESC")
    return render_template('admin/contacts.html', items=items)

@admin_bp.route('/contacts/read/<int:id>')
@admin_required
def contact_read(id):
    query("UPDATE contacts SET is_read=1 WHERE id=%s", (id,), commit=True)
    return redirect(url_for('admin.contacts'))

@admin_bp.route('/contacts/delete/<int:id>', methods=['POST'])
@admin_required
def contact_delete(id):
    query("DELETE FROM contacts WHERE id=%s", (id,), commit=True)
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.contacts'))

# --- Users ---
@admin_bp.route('/users')
@admin_required
def users():
    items = query("SELECT id,name,email,role,created_at FROM users ORDER BY created_at DESC")
    return render_template('admin/users.html', items=items)
