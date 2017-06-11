from typing import Dict

from flask import jsonify, Blueprint, make_response

from project import db
from project.models import Task


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = [mapped_data(result) for result in results]
    return jsonify(items=json_results)


@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id: int):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        result = {
            'task_id': result.task_id,
            'task_name': result.name,
            'due_date': str(result.due_date),
            'priority': result.priority,
            'posted_date': str(result.posted_date),
            'status': result.status,
            'user_id': result.user_id
        }
        code = 200
    else:
        result = {'error': 'Element does not exist.'}
        code = 404
    return make_response(jsonify(result), code)


def mapped_data(result: Task) -> Dict:
    data = {
        'task_id': result.task_id,
        'task_name': result.name,
        'due_date': str(result.due_date),
        'priority': result.priority,
        'posted_date': str(result.posted_date),
        'status': result.status,
        'user_id': result.user_id
    }
    return data
