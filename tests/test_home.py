import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from flask_testing import TestCase
from app import create_app, database
from app.models import User, Claim, Service
import datetime

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config")
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        database.create_all()
    
    def tearDown(self):
        database.session.remove()
        database.drop_all()

class TestHomeBlueprint(BaseTestCase):
    def test_all_users(self):
        # Create a test user
        user = User(name="Test User", gender="Male", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        response = self.client.get('/home/all/users')
        self.assert200(response)
        self.assertIn(b"Test User", response.data)  # Assuming the template renders user names

    def test_view_user(self):
        user = User(name="Test User", gender="Male", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        response = self.client.get(f'/home/user/{user.id}')
        self.assert200(response)
        self.assertIn(b"Test User", response.data)

    def test_edit_user(self):
        user = User(name="Test User", gender="Male", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        # Test GET method
        response = self.client.get(f'/home/user/{user.id}/edit')
        self.assert200(response)
        
        # Test POST method
        response = self.client.post(f'/home/user/{user.id}/edit', data={
            'name': 'Updated User',
            'gender': 'F',
            'salary': '60000',
            'date_of_birth': '1991-01-01'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"User updated successfully.", response.data)
        updated_user = User.query.get(user.id)
        self.assertEqual(updated_user.name, "Updated User")
        self.assertEqual(updated_user.gender, "F")

    def test_add_user(self):
        response = self.client.post('/home/users/add', data={
            'name': 'New User',
            'gender': 'M',
            'salary': '70000',
            'date_of_birth': '1980-01-01'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"User created successfully.", response.data)
        new_user = User.query.filter_by(name='New User').first()
        self.assertIsNotNone(new_user)

    def test_delete_user(self):
        user = User(name="ToDelete", gender="Male", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        response = self.client.post(f'/home/user/{user.id}/delete', follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"User deleted successfully.", response.data)
        self.assertIsNone(User.query.get(user.id))

    def test_claim(self):
        claim = Claim(user_id=1, diagnosis="Test", hmo="HMO", age=30, service_charge=100, total_cost=200, final_cost=150)
        database.session.add(claim)
        database.session.commit()
        
        response = self.client.get('/home/claim')
        self.assert200(response)
        self.assertIn(b"Test", response.data)  # Assuming the template renders diagnosis

    def test_claim_detail(self):
        claim = Claim(user_id=1, diagnosis="Test", hmo="HMO", age=30, service_charge=100, total_cost=200, final_cost=150)
        database.session.add(claim)
        database.session.commit()
        
        # Test GET method
        response = self.client.get(f'/home/claim/{claim.id}/')
        self.assert200(response)
        
        # Test PUT method (Flask-Testing doesn't handle PUT easily, so we simulate via POST)
        response = self.client.post(f'/home/claim/{claim.id}/', data={
            'diagnosis': 'Updated Diagnosis',
            'hmo': 'Updated HMO',
            'age': '35',
            'service_charge': '150',
            'total_cost': '250',
            'final_cost': '200'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"Claim updated successfully!", response.data)
        updated_claim = Claim.query.get(claim.id)
        self.assertEqual(updated_claim.diagnosis, "Updated Diagnosis")

        # Test DELETE method (simulated via POST)
        response = self.client.post(f'/home/claim/{claim.id}/', data={'_method': 'DELETE'}, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"Claim deleted successfully!", response.data)
        self.assertIsNone(Claim.query.get(claim.id))

    def test_create_claim(self):
        user = User(name="Claim User", gender="Male", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        response = self.client.post('/home/create_claim', data={
            'user': 'Claim User',
            'diagnosis': 'Test Diagnosis',
            'hmo': 'Test HMO',
            'age': '30',
            'total_cost': '200',
            'service_charge': '100',
            'final_cost': '150',
            'service_name': ['Service1'],
            'type': ['Type1'],
            'provider_name': ['Provider1'],
            'source': ['Source1'],
            'cost_of_service': ['50'],
            'service_date': ['2023-01-01']
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"Claim created successfully.", response.data)
        new_claim = Claim.query.filter_by(diagnosis='Test Diagnosis').first()
        self.assertIsNotNone(new_claim)
        service = Service.query.filter_by(claim_id=new_claim.id).first()
        self.assertIsNotNone(service)

    def test_user_age(self):
        user = User(name="Age User", gender="M", salary="50000", date_of_birth=datetime.date(1990, 1, 1))
        database.session.add(user)
        database.session.commit()
        
        response = self.client.post('/home/create_claim/user_details/', json={"name": "Age User"})
        self.assert200(response)
        data = response.json
        self.assertEqual(data['age'], datetime.date.today().year - 1990)
        self.assertEqual(data['gender'], 'M')

if __name__ == '__main__':
    pytest.main()