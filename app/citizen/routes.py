import functools
from flask import render_template, redirect, url_for, flash, request, g, session
from app.db import get_db
from app.auth.routes import login_required
from app.citizen import bp

def citizen_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        if g.user['role'] != 'Citizen':
            flash('Access restricted to Citizens only.', 'danger')
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return wrapped_view

@bp.route('/dashboard')
@login_required
@citizen_required
def dashboard():
    db = get_db()
    # Fetch citizen's requests
    requests_list = db.execute(
        'SELECT * FROM rescue_requests WHERE user_id = ? ORDER BY created_at DESC',
        (g.user['id'],)
    ).fetchall()
    
    # Calculate stats
    stats = {
        'total': len(requests_list),
        'pending': sum(1 for r in requests_list if r['status'] == 'Pending'),
        'in_progress': sum(1 for r in requests_list if r['status'] == 'In Progress'),
        'resolved': sum(1 for r in requests_list if r['status'] == 'Resolved')
    }
    
    return render_template('citizen/dashboard.html', requests=requests_list, stats=stats)

@bp.route('/request', methods=('GET', 'POST'))
@login_required
@citizen_required
def request_rescue():
    if request.method == 'POST':
        location = request.form['location'].strip()
        latitude = request.form['latitude'].strip() or None
        longitude = request.form['longitude'].strip() or None
        details = request.form['details'].strip()
        
        error = None

        if not location:
            error = 'Location is required.'
        elif not details:
            error = 'Emergency details are required.'

        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO rescue_requests (user_id, location, latitude, longitude, details) VALUES (?, ?, ?, ?, ?)',
                (g.user['id'], location, latitude, longitude, details)
            )
            db.commit()
            flash('Your emergency rescue request has been successfully submitted.', 'success')
            return redirect(url_for('citizen.dashboard'))
            
        flash(error, 'error')

    return render_template('citizen/request.html')
