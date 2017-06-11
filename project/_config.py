import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = b'w\n\xb1_\x88F0\x19\xaa\xb5M\x84!\xb8\xe7\xf2_\x8d\xa6\xb1\xbe\xe6\x7f8'
WTF_CSRF_SECRET_KEY = b'w\n\xb1_\x88F0\x19\xaa\xb5M\x84!\xb8\xe7\xf2_\x8d\xa6\xb1\xbe\xe6\x7f8'
DEBUG = False

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
