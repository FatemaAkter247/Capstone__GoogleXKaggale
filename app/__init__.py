import os
from flask import Flask, render_template, session, redirect, url_for

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Defaults
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-resqlink'),
        DATABASE=os.path.join(app.instance_path, os.environ.get('DATABASE', 'resqlink.db')),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth, citizen, ai, shelter, rescue, alerts, resources, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(citizen.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(shelter.bp)
    app.register_blueprint(rescue.bp)
    app.register_blueprint(alerts.bp)
    app.register_blueprint(resources.bp)
    app.register_blueprint(admin.bp)

    # Smart role-based root routing
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        role = session.get('role')
        if role == 'Citizen':
            return redirect(url_for('citizen.dashboard'))
        elif role == 'System Admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'Shelter Admin':
            return redirect(url_for('shelter.index'))
        elif role == 'Rescue Team':
            return redirect(url_for('rescue.index'))
        return render_template('index.html')

    return app
