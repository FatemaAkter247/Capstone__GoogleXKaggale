from flask import render_template, redirect, url_for, flash, request, g
from app.db import get_db
from app.auth.routes import login_required
from app.rescue import bp

@bp.route('/')
@login_required
def index():
    db = get_db()
    if g.user['role'] == 'Citizen':
        requests_list = db.execute(
            'SELECT r.*, u.username FROM rescue_requests r JOIN users u ON r.user_id=u.id WHERE r.user_id=? ORDER BY r.created_at DESC',
            (g.user['id'],)
        ).fetchall()
    else:
        requests_list = db.execute(
            'SELECT r.*, u.username FROM rescue_requests r JOIN users u ON r.user_id=u.id ORDER BY r.created_at DESC'
        ).fetchall()
    return render_template('rescue/index.html', requests=requests_list)

@bp.route('/update/<int:id>', methods=('POST',))
@login_required
def update(id):
    if g.user['role'] not in ('Rescue Team', 'System Admin'):
        flash('Access denied.', 'danger')
        return redirect(url_for('rescue.index'))
    status = request.form.get('status')
    priority = request.form.get('priority')
    db = get_db()
    db.execute('UPDATE rescue_requests SET status=?, priority=? WHERE id=?', (status, priority, id))
    db.commit()
    flash('Request updated.', 'success')
    return redirect(url_for('rescue.index'))
