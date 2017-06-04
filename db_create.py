from datetime import date

from project import db
from project.models import Task, User

db.create_all()

db.session.add(User('admin', 'ad@min.com', 'admin', 'admin'))
db.session.add(
	Task('Finish this tutorial', date(2017, 6, 2), 10, date(2017, 6, 2), 1, 1)
)
db.session.add(
	Task('Finish Real Python', date(2017, 9, 13), 10, date(2017, 6, 2), 1, 1)
)

db.session.commit()
