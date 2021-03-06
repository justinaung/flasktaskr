import unittest

from setup_test import SetupTests
from project.models import User
from project import db


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

    def test_task_template_displays_logged_in_username(self):
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        self.login('Fletcher', 'python101')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Fletcher', response.data)

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        response = self.login('Fletcher', 'python101')
        self.assertNotIn(b'Mark as complete', response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'complete/2/', response.data)

    def test_admin_users_can_see_task_modify_links_for_all_links(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)


if __name__ == '__main__':
    unittest.main()
