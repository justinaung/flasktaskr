from functools import wraps
import datetime

from flask import (flash,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)

from forms import AddTaskForm, RegisterForm, LoginForm
from models import Task, User
from _config import db, app


# helper functions

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
    return wrap


# route handlers

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                name=form.name.data,
            ).first()
            if user is not None and user.password == form.password.data:
                session['logged_in'] = True
                session['user_id'] = user.id
                flash('Welcome!')
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid Credentials. Please try again.'
        else:
            error = 'Both fields are required.'
    return render_template('login.html', form=form, error=error)


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
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        else:
            error = form.errors

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
    else:
        flash('All fields are required.')
    return render_template('tasks.html', form=form)


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({'status': 0})
    db.session.commit()
    flash('The task is complete. Nice.')
    return redirect(url_for('tasks'))


@app.route('/incomplete/<int:task_id>/')
@login_required
def incomplete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({'status': 1})
    db.session.commit()
    flash("What? You didn't finish it?")
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task has been deleted.')
    return redirect(url_for('tasks'))
