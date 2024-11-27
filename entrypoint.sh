#!/bin/bash
source $VIRTUAL_ENV/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0