#!/bin/sh

python3 manage.py migrate
python3 manage.py test tests/unit
python3 manage.py test tests/integration
