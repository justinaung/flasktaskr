import unittest

from setup_test import SetupTests


class MainTests(SetupTests):

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Sorry. There\'s nothing here.", response.data)


if __name__ == '__main__':
    unittest.main()
