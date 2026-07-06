from flask import render_template, redirect, url_for, flash, request, g
from app.db import get_db
from app.auth.routes import login_required
from app.resources import bp

@bp.route('/')
@login_required
def index():
    db = get_db()
    resources = db.execute(
        'SELECT r.*, s.name as shelter_name FROM resources r LEFT JOIN shelters s ON r.shelter_id=s.id ORDER BY r.category'
    ).fetchall()
    return render_template('resources/index.html', resources=resources)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if g.user['role'] not in ('Shelter Admin', 'System Admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('resources.index'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        category = request.form['category']
        quantity = request.form['quantity']
        unit = request.form['unit'].strip() or 'units'
        shelter_id = request.form.get('shelter_id') or None
        error = None
        if not name: error = 'Resource name required.'
        elif not quantity: error = 'Quantity required.'
        if error is None:
            db = get_db()
            db.execute('INSERT INTO resources (name, category, quantity, unit, shelter_id) VALUES (?,?,?,?,?)',
                       (name, category, int(quantity), unit, shelter_id))
            db.commit()
            flash('Resource added.', 'success')
            return redirect(url_for('resources.index'))
        flash(error, 'error')
    db = get_db()
    shelters = db.execute('SELECT id, name FROM shelters').fetchall()
    return render_template('resources/add.html', shelters=shelters)

@bp.route('/update/<int:id>', methods=('POST',))
@login_required
def update(id):
    if g.user['role'] not in ('Shelter Admin', 'System Admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('resources.index'))
    quantity = request.form.get('quantity', 0)
    db = get_db()
    db.execute('UPDATE resources SET quantity=?, last_updated=CURRENT_TIMESTAMP WHERE id=?', (quantity, id))
    db.commit()
    flash('Resource quantity updated.', 'success')
    return redirect(url_for('resources.index'))
