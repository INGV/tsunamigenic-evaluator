# -*- coding: utf-8 -*-
""" Web Server Gateway Interface  """

import os

from main.api import create_app_blueprint

# create and load `.env` file here from the respective environment to overwrite the env settings
# before app is created.

application = create_app_blueprint(os.getenv('FLASK_CONFIG') or 'default')
