import unittest
import os
import json
from app import create_app
from app.db import get_db, init_db

class AITestCase(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_ai_resqlink.db'
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        self.client = self.app.test_client()
        
        with self.app.app_context():
            init_db()
            
            # Create a test Citizen user
            from werkzeug.security import generate_password_hash
            db = get_db()
            db.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                ('citizen_tester', 'tester@test.com', generate_password_hash('password123'), 'Citizen')
            )
            db.commit()

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def login(self):
        return self.client.post('/auth/login', data=dict(
            username_or_email='citizen_tester',
            password='password123'
        ), follow_redirects=True)

    def test_ai_routes_authentication(self):
        # 1. Unauthenticated users cannot access chat
        response = self.client.get('/ai/chat', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

        # 2. Unauthenticated users cannot access checklist
        response = self.client.get('/ai/checklist', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_ai_chat_fallback(self):
        # Log in
        self.login()

        # Test normal chat response (triggers the fallback guidance because GEMINI_API_KEY is empty/unset in test env)
        response = self.client.post('/ai/chat', 
            data=json.dumps({'message': 'How do I handle a flood?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Showing mock disaster guidance', data['response'])
        self.assertIn('Avoid Hazard Areas', data['response'])

    def test_ai_chat_shelter_intent(self):
        # Log in
        self.login()

        # Ask a query containing shelter keywords
        response = self.client.post('/ai/chat', 
            data=json.dumps({'message': 'Where is the nearest shelter?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Even with mock fallback, we verify it executes correctly
        self.assertIsNotNone(data['response'])

    def test_checklist_generation(self):
        # Log in
        self.login()

        # GET request
        response = self.client.get('/ai/checklist')
        self.assertEqual(response.status_code, 200)

        # POST request to generate checklist
        response = self.client.post('/ai/checklist', data=dict(
            disaster_type='Flood'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Action Checklist: Flood', response.data)
        self.assertIn(b'Avoid Hazard Areas', response.data)

if __name__ == '__main__':
    unittest.main()
