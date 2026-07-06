from flask import render_template, redirect, url_for, flash, request, g
from app.db import get_db
from app.auth.routes import login_required
from app.alerts import bp

@bp.route('/')
@login_required
def index():
    db = get_db()
    active = db.execute('SELECT * FROM disaster_alerts WHERE is_active=1 ORDER BY created_at DESC').fetchall()
    archived = db.execute('SELECT * FROM disaster_alerts WHERE is_active=0 ORDER BY created_at DESC').fetchall()
    return render_template('alerts/index.html', active_alerts=active, archived_alerts=archived)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if g.user['role'] != 'System Admin':
        flash('Only System Admins can post alerts.', 'danger')
        return redirect(url_for('alerts.index'))
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        severity = request.form['severity']
        area = request.form['area'].strip()
        error = None
        if not title: error = 'Title required.'
        elif not description: error = 'Description required.'
        elif not area: error = 'Affected area required.'
        if error is None:
            db = get_db()
            db.execute('INSERT INTO disaster_alerts (title, description, severity, area, created_by) VALUES (?,?,?,?,?)',
                       (title, description, severity, area, g.user['id']))
            db.commit()
            flash('Alert posted successfully.', 'success')
            return redirect(url_for('alerts.index'))
        flash(error, 'error')
    return render_template('alerts/add.html')

@bp.route('/deactivate/<int:id>')
@login_required
def deactivate(id):
    if g.user['role'] != 'System Admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('alerts.index'))
    db = get_db()
    db.execute('UPDATE disaster_alerts SET is_active=0 WHERE id=?', (id,))
    db.commit()
    flash('Alert archived.', 'info')
    return redirect(url_for('alerts.index'))
