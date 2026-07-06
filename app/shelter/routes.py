from flask import render_template, redirect, url_for, flash, request, g
from app.db import get_db
from app.auth.routes import login_required
from app.shelter import bp

@bp.route('/')
@login_required
def index():
    db = get_db()
    shelters = db.execute('SELECT * FROM shelters ORDER BY name').fetchall()
    return render_template('shelter/index.html', shelters=shelters)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if g.user['role'] not in ('Shelter Admin', 'System Admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('shelter.index'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        location = request.form['location'].strip()
        capacity = request.form['capacity']
        latitude = request.form.get('latitude') or None
        longitude = request.form.get('longitude') or None
        error = None
        if not name: error = 'Name is required.'
        elif not location: error = 'Location is required.'
        elif not capacity: error = 'Capacity is required.'
        if error is None:
            db = get_db()
            db.execute('INSERT INTO shelters (name, location, capacity, latitude, longitude) VALUES (?,?,?,?,?)',
                       (name, location, int(capacity), latitude, longitude))
            db.commit()
            flash('Shelter added successfully.', 'success')
            return redirect(url_for('shelter.index'))
        flash(error, 'error')
    return render_template('shelter/add.html')

@bp.route('/update/<int:id>', methods=('POST',))
@login_required
def update(id):
    if g.user['role'] not in ('Shelter Admin', 'System Admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('shelter.index'))
    occupancy = request.form.get('occupancy', 0)
    status = request.form.get('status', 'Open')
    db = get_db()
    db.execute('UPDATE shelters SET current_occupancy=?, status=? WHERE id=?', (occupancy, status, id))
    db.commit()
    flash('Shelter updated.', 'success')
    return redirect(url_for('shelter.index'))
