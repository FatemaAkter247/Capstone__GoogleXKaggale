import unittest
import os
from app import create_app
from app.db import get_db, init_db

class CitizenTestCase(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_citizen_resqlink.db'
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        self.client = self.app.test_client()
        
        with self.app.app_context():
            init_db()
            
            # Setup users for roles testing
            db = get_db()
            # Register a Citizen
            from werkzeug.security import generate_password_hash
            db.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                ('citizen_user', 'citizen@test.com', generate_password_hash('password123'), 'Citizen')
            )
            # Register a non-citizen (Rescue Team)
            db.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                ('rescue_user', 'rescue@test.com', generate_password_hash('password123'), 'Rescue Team')
            )
            db.commit()

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def login(self, username_or_email, password):
        return self.client.post('/auth/login', data=dict(
            username_or_email=username_or_email,
            password=password
        ), follow_redirects=True)

    def test_citizen_dashboard_access(self):
        # 1. Unauthenticated redirect to login
        response = self.client.get('/citizen/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

        # 2. Login as Citizen and access dashboard
        self.login('citizen_user', 'password123')
        response = self.client.get('/citizen/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, citizen_user', response.data)

        # 3. Login as Rescue Team and verify citizen dashboard is restricted
        self.client.get('/auth/logout', follow_redirects=True)
        self.login('rescue_user', 'password123')
        response = self.client.get('/citizen/dashboard', follow_redirects=True)
        self.assertIn(b'Access restricted to Citizens only.', response.data)

    def test_submit_rescue_request(self):
        # Log in as Citizen
        self.login('citizen_user', 'password123')

        # Submit a rescue request
        response = self.client.post('/citizen/request', data=dict(
            location='Sector 4, Building 10',
            latitude='23.815',
            longitude='90.420',
            details='Water levels rising, family trapped on the second floor.'
        ), follow_redirects=True)

        self.assertIn(b'Your emergency rescue request has been successfully submitted.', response.data)

        # Check database entry
        with self.app.app_context():
            db = get_db()
            req = db.execute('SELECT * FROM rescue_requests WHERE location = ?', ('Sector 4, Building 10',)).fetchone()
            self.assertIsNotNone(req)
            self.assertEqual(req['details'], 'Water levels rising, family trapped on the second floor.')
            self.assertEqual(req['latitude'], 23.815)
            self.assertEqual(req['longitude'], 90.420)
            self.assertEqual(req['status'], 'Pending')
            self.assertEqual(req['priority'], 'Medium')

if __name__ == '__main__':
    unittest.main()
