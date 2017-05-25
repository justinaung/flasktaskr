from _config import db
from models import Task
from datetime import date


db.create_all()

# db.session.add(Task('Finish this tutorial', date(2017, 5, 14), 10, 1))
# db.session.add(Task('Finish Real Python', date(2017, 7, 22), 10, 1))

# db.session.commit()
