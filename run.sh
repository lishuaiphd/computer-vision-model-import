#!/usr/bin/env bash
export FLASK_APP=app.py
export FLASK_ENV=development
mkdir -p uploads
python -u app.py