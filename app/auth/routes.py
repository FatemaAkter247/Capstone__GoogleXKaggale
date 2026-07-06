import functools
from flask import render_template, redirect, url_for, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db
from app.auth import bp

# Allowed user roles
ROLES = ['Citizen', 'Shelter Admin', 'Rescue Team', 'System Admin']

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif role not in ROLES:
            error = 'Invalid role selected.'
        else:
            # Check if user already exists
            user_exists = db.execute(
                'SELECT id FROM users WHERE username = ? OR email = ?', (username, email)
            ).fetchone()
            if user_exists:
                error = 'Username or Email is already registered.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                    (username, email, generate_password_hash(password), role)
                )
                db.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                error = 'Database error: Username or Email already exists.'

        flash(error, 'error')

    return render_template('auth/register.html', roles=ROLES)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email'].strip()
        password = request.form['password']
        db = get_db()
        error = None

        # Allow logging in with either username or email
        user = db.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username_or_email, username_or_email)
        ).fetchone()

        if user is None:
            error = 'Incorrect username, email, or password.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect username, email, or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
