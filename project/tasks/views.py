import datetime

from flask import (flash, redirect, render_template, request, session, url_for,
                   Blueprint)

from .forms import AddTaskForm
from project import db
from project.models import Task
from project.common import utils


tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route('/tasks/')
@utils.login_required
def tasks():
    return render_template('tasks.html',
                           form=AddTaskForm(request.form),
                           open_tasks=utils.open_tasks(),
                           closed_tasks=utils.closed_tasks(),
                           username=session['username'])


@tasks_blueprint.route('/add/', methods=['POST'])
@utils.login_required
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
        return redirect(url_for('tasks.tasks'))
    return render_template('tasks.html',
                           form=form,
                           open_tasks=utils.open_tasks(),
                           closed_tasks=utils.closed_tasks())


@tasks_blueprint.route('/complete/<int:task_id>/')
@utils.login_required
def complete(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.update({'status': 0})
        db.session.commit()
        flash('The task is complete. Nice.')
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/incomplete/<int:task_id>/')
@utils.login_required
def incomplete(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.update({'status': 1})
        db.session.commit()
        flash("What? You didn't finish it?")
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/delete/<int:task_id>/')
@utils.login_required
def delete_entry(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    is_task_owner = session['user_id'] == task.first().user_id
    if is_task_owner or session['role'] == 'admin':
        task.delete()
        db.session.commit()
        flash('The task has been deleted.')
    else:
        flash('You can only delete tasks that belong to you.')
    return redirect(url_for('tasks.tasks'))
