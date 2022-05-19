#!/bin/bash
flask db migrate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:'create_app()'