import sqlite3
# from datetime import datetime

from _config import DATABASE_PATH
from views import db


# with sqlite3.connect(DATABASE_PATH) as connection:
#     c = connection.cursor()
#
#     # temporarily change the name of tasks table
#     c.execute('ALTER TABLE tasks RENAME to old_tasks')
#
#     # recreate a new tasks table with updated schema
#     db.create_all()
#
#     # retrieve data from old_tasks table
#     c.execute("""SELECT name, due_date, priority, status
#                  FROM old_tasks ORDER BY task_id ASC""")
#
#     # save all rows as a list of tuples; set posted_date to now and user_id to 1
#     data = [
#         (row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()
#     ]
#
#     # insert data to tasks table
#     c.executemany("""
#         INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id)
#         VALUES (?, ?, ?, ?, ?, ?)""", data)
#
#     # delete old_tasks table
#     c.execute('DROP TABLE old_tasks')

with sqlite3.connect(DATABASE_PATH) as connection:

    c = connection.cursor()

    c.execute('ALTER TABLE users RENAME to old_users')

    db.create_all()

    c.execute('SELECT name, email, password FROM old_users ORDER BY id ASC')

    data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

    c.executemany(
        'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
        data
    )

    c.execute('DROP TABLE old_users')
