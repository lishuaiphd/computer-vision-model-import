@echo off
set FLASK_APP=app.py
set FLASK_ENV=development
if not exist uploads mkdir uploads
python -u app.py
pause