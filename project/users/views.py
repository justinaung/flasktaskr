from functools import wraps
from flask import (flash, redirect, render_template, request, session,
                   url_for, Blueprint)
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db
from project.models import User


users_blueprint = Blueprint('users', __name__)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            return redirect(url_for('users.login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            label = getattr(form, field).label.text
            flash(f'Error in the {label} field - {error}')


@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('Goodbye!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                name=form.name.data,
            ).first()

            if (user is not None and
                    user.is_correct_password(form.password.data)):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.name
                session['role'] = user.role
                flash('Welcome!')
                return redirect(url_for('tasks.tasks'))
            else:
                error = 'Invalid Credentials. Please try again.'
                flash(error)
    flash_errors(form)
    return render_template('login.html', form=form)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():

            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'That username and/or email already exists.'
                return render_template('register.html', form=form, error=error)
    flash_errors(form)
    return render_template('register.html', form=form, error=error)
