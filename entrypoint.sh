#!/bin/sh

# Below shells script is required because the flask container need to wait for postgres db server to startup before
# accessing it below.

# Run below commands from manage.py to initialize db and have some default data.
uwsgi --ini /etc/uwsgi.ini