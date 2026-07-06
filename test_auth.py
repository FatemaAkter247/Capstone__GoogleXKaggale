import unittest
from app import create_app
from app.db import get_db, init_db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        import os
        self.db_path = 'test_resqlink.db'
        # Configure app for testing
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        self.client = self.app.test_client()
        
        # Initialize the database
        with self.app.app_context():
            init_db()

    def tearDown(self):
        import os
        # Delete test database file if it exists
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def register(self, username, email, password, role):
        return self.client.post('/auth/register', data=dict(
            username=username,
            email=email,
            password=password,
            role=role
        ), follow_redirects=True)

    def login(self, username_or_email, password):
        return self.client.post('/auth/login', data=dict(
            username_or_email=username_or_email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_registration_and_login_flow(self):
        # 1. Test registration of a Citizen
        response = self.register('citizen_test', 'citizen@test.com', 'password123', 'Citizen')
        self.assertIn(b'Registration successful! Please log in.', response.data)

        # 2. Test duplicate registration
        response = self.register('citizen_test', 'another@test.com', 'password123', 'Citizen')
        self.assertIn(b'Username or Email is already registered.', response.data)

        # 3. Test registration with invalid role
        response = self.register('bad_role_user', 'bad@test.com', 'password123', 'SuperAdmin')
        self.assertIn(b'Invalid role selected.', response.data)

        # 4. Test login
        response = self.login('citizen_test', 'password123')
        self.assertIn(b'Welcome back, citizen_test!', response.data)
        self.assertIn(b'Welcome to ResQLink', response.data)

        # 5. Test login with email
        self.logout()
        response = self.login('citizen@test.com', 'password123')
        self.assertIn(b'Welcome back, citizen_test!', response.data)

        # 6. Test login with wrong password
        self.logout()
        response = self.login('citizen_test', 'wrongpassword')
        self.assertIn(b'Incorrect username, email, or password.', response.data)

        # 7. Test logout
        response = self.logout()
        self.assertIn(b'You have been logged out successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
