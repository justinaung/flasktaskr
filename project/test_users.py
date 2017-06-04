import unittest

from setup_test import SetupTests
from models import User
from views import db


class UserTests(SetupTests):

    def test_user_setup(self):
        new_user = User('micheal', 'micheal@mherman.org', 'michaelherman')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'micheal'

    def test_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list.', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    def test_users_can_login(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('Michael', 'python')
        self.assertIn(b'Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('alert("alert box!")', 'foo')
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Micheal', 'michael@realpython.com', 'python', 'python'
        )
        self.assertIn(b'That username and/or email already exists.',
                      response.data)

    def test_logged_in_users_can_logout(self):
        self.register('Fletcher', 'fletcher@realpython.com', 'python', 'python')
        self.login('Fletcher', 'python')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye', response.data)

    def test_default_user_role(self):
        db.session.add(
            User('Johnny', 'john@doe.com', 'johnny')
        )
        db.session.commit()

        users = db.session.query(User).all()
        print(users)
        for user in users:
            self.assertEqual(user.role, 'user')


if __name__ == '__main__':
    unittest.main()
