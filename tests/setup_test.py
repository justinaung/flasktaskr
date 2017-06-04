import os
import unittest

from project import app, db
from project._config import basedir
from project.models import User


TEST_DB = 'test.db'


class SetupTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:////' +
                                                 os.path.join(basedir, TEST_DB))
        self.app = app.test_client()
        db.create_all()

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

    @staticmethod
    def create_user(name, email, password):
        new_user = User(name=name, email=email, password=password)
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

    @staticmethod
    def create_admin_user():
        new_user = User(
            name='Superman',
            email='admin@realpython.com',
            password='allpowerful',
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()
