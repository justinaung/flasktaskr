from functools import wraps

from flask import (flash,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)

from forms import AddTaskForm
from models import Task
from _config import db


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
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('tasks'))
    return render_template('login.html')


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
                        1)
        db.session.add(new_task)
        db.session.commit()
        flash('New entry has been successfully posted. Thanks.')

    return redirect(url_for('tasks'))


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
