from functools import wraps

from flask import session, redirect, url_for

from project import db
from project.models import Task


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('users.login'))
    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(
        status=1).order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status=0).order_by(Task.due_date.asc())
