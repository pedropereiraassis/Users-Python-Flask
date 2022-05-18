import os
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URL = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
JWT_SECRET_KEY='1234'
FLASK_APP='app'
FLASK_ENV='development'