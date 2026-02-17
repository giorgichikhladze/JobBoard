import unittest
from main import app, db
from models import User, Job
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class JobBoardTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context(): # ვქმნი სატესტო იუზერი
            db.create_all()
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            user = User(username='TestUser', email='test@test.com', password=hashed_pw)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_logic(self):
        response = self.app.post('/login', data=dict(
            email='test@test.com', password='wrongpassword'
        ), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertIn("თქვენ ვერ შეხვედით".encode('utf-8'), response.data)

    def test_unauthorized_delete(self):
        # ვცდილობ წაშლას ავტორიზაციის გარეშე
        response = self.app.post('/job/1/delete', follow_redirects=True)
        # ამან უნდა მოგვთხოვოს ავტორიზაცია
        self.assertIn("login", response.request.path.lower())

if __name__ == '__main__':
    unittest.main()