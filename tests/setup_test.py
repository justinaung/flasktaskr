import unittest

from project import app, db
from project.models import User


class SetupTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test'
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    @staticmethod
    def tearDown():
        db.session.remove()
        db.drop_all()

    ##################
    # Helper methods #
    ##################
    def login(self, name, password):
        return self.app.post('/',
                             data=dict(name=name, password=password),
                             follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password, role=None):
        new_user = User(name, email, password, role)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='10/08/2017',
            priority='1',
            posted_date='31/05/2017',
            status=1),
            follow_redirects=True
        )

    def create_admin_user(self):
        self.create_user('Superman',
                         'admin@realpython.com',
                         'allpowerful',
                         'admin')
