#!/bin/bash
# Quick run for development
export FLASK_APP=wsgi.py
export FLASK_ENV=development
# Use DATABASE_URL if set. Otherwise sqlite in instance/.
python -m venv venv || true
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
flask run --host=0.0.0.0
