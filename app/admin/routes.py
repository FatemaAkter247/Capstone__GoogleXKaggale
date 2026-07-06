import functools
from flask import render_template, redirect, url_for, flash, g
from app.db import get_db
from app.auth.routes import login_required
from app.admin import bp

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None or g.user['role'] != 'System Admin':
            flash('System Admin access required.', 'danger')
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return wrapped_view

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    db = get_db()
    stats = {
        'total_users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'citizens': db.execute("SELECT COUNT(*) FROM users WHERE role='Citizen'").fetchone()[0],
        'rescue_team': db.execute("SELECT COUNT(*) FROM users WHERE role='Rescue Team'").fetchone()[0],
        'shelter_admins': db.execute("SELECT COUNT(*) FROM users WHERE role='Shelter Admin'").fetchone()[0],
        'total_requests': db.execute('SELECT COUNT(*) FROM rescue_requests').fetchone()[0],
        'pending_requests': db.execute("SELECT COUNT(*) FROM rescue_requests WHERE status='Pending'").fetchone()[0],
        'critical_requests': db.execute("SELECT COUNT(*) FROM rescue_requests WHERE priority='Critical'").fetchone()[0],
        'active_alerts': db.execute('SELECT COUNT(*) FROM disaster_alerts WHERE is_active=1').fetchone()[0],
        'total_shelters': db.execute('SELECT COUNT(*) FROM shelters').fetchone()[0],
        'open_shelters': db.execute("SELECT COUNT(*) FROM shelters WHERE status='Open'").fetchone()[0],
    }
    recent_requests = db.execute(
        'SELECT r.*, u.username FROM rescue_requests r JOIN users u ON r.user_id=u.id ORDER BY r.created_at DESC LIMIT 10'
    ).fetchall()
    users = db.execute('SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC').fetchall()
    alerts = db.execute('SELECT * FROM disaster_alerts ORDER BY created_at DESC LIMIT 5').fetchall()
    return render_template('admin/dashboard.html', stats=stats, recent_requests=recent_requests, users=users, alerts=alerts)
