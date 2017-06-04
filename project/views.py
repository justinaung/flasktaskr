from functools import wraps
import datetime

from flask import (Flask,
                   flash,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy

from forms import AddTaskForm, RegisterForm, LoginForm

# config
app = Flask(__name__)
CSRFProtect(app)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User


# helper functions

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


# route handlers

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                name=form.name.data,
            ).first()
            if user is not None and user.password == form.password.data:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                flash('Welcome!')
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid Credentials. Please try again.'
                flash(error)
    flash_errors(form)
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
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
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'That username and/or email already exists.'
                return render_template('register.html', form=form, error=error)
    flash_errors(form)
    return render_template('register.html', form=form, error=error)


@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = (db.session.query(Task)
                  .filter_by(status=1)
                  .order_by(Task.due_date.asc()))
    closed_tasks = (db.session.query(Task)
                    .filter_by(status=0)
                    .order_by(Task.due_date.asc()))

    return render_template('tasks.html',
                           form=AddTaskForm(request.form),
                           open_tasks=open_tasks,
                           closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if form.validate_on_submit():
        new_task = Task(form.name.data,
                        form.due_date.data,
                        form.priority.data,
                        datetime.datetime.utcnow(),
                        1,
                        session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('New entry has been successfully posted. Thanks.')
        return redirect(url_for('tasks'))
    return render_template('tasks.html',
                           form=form,
                           open_tasks=open_tasks(),
                           closed_tasks=closed_tasks())


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.update({'status': 0})
        db.session.commit()
        flash('The task is complete. Nice.')
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks'))


@app.route('/incomplete/<int:task_id>/')
@login_required
def incomplete(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.update({'status': 1})
        db.session.commit()
        flash("What? You didn't finish it?")
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.delete()
        db.session.commit()
        flash('The task has been deleted.')
    else:
        flash('You can only delete tasks that belong to you.')
    return redirect(url_for('tasks'))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            label = getattr(form, field).label.text
            flash(f'Error in the {label} field - {error}')


def open_tasks():
    return db.session.query(Task).filter_by(
        status=1).order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status=0).order_by(Task.due_date.asc())
