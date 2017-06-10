import unittest

from setup_test import SetupTests
from project.models import User
from project import db


class MainTests(SetupTests):

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Sorry. There\'s nothing here.", response.data)

    def test_500_error(self):
        bad_user = User(
            name='Jeremy', email='jeremy@realpython.com', password='django'
        )
        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'Jeremy', 'django')
        try:
            response = self.login('Jeremy', 'django')
        except ValueError:
            pass
        else:
            self.assertEqual(response.status_code, 500)
            self.assertNotIn(b'ValueError: Invalid salt', response.data)
            self.assertIn(b'Something went terribly wrong.', response.data)


if __name__ == '__main__':
    unittest.main()
