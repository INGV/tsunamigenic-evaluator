# -*- coding: utf-8 -*-
"""Angular-Flask-Docker-Skeleton

    Main application package

"""

from flask import Flask
#from flask_caching import Cache
import logging
import logging.handlers
from main.utils.common import register_blueprints
from settings import config
from pathlib import Path
import sys
import os


logger = None
cache = None

def create_logger(app_settings):
    global logger
    log_name = Path(__file__).stem
    logger = logging.getLogger(log_name)

    formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    numeric_level = getattr(logging, app_settings.LOG_SEVERITY, 'INFO')
    logger.setLevel(numeric_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    log_folder = './log'
    if not os.path.isdir(log_folder):
        os.makedirs(log_folder, 493)

    log_file_name = os.path.join(log_folder, 'tsunamigenic-evaluator.log')
    f_handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=1000000, backupCount=10)
    f_handler.setLevel(numeric_level)
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)
    #return logger

# def create_cache(app_settings, app):
#     cache_dir = app_settings.CACHE_DIR
#     if not os.path.exists(cache_dir):
#         os.makedirs(cache_dir, 0o755)
#
#     cache = Cache(app, config={'CACHE_TYPE': 'filesystem',
#                            'CACHE_DIR': cache_dir,
#                            'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
#                            'CACHE_THRESHOLD': 922337203685477580})
#     return cache

def create_app(config_type, package_name, package_path):
    # global logger
    global cache
    app = Flask(__name__, instance_relative_config=True)
    # set default config
    # app_settings = os.getenv('APP_DEV_SETTINGS')
    app_settings = config[config_type]
    app.config.from_object(app_settings)
    #logger = create_logger(app_settings)
    create_logger(app_settings)
    logger.info(f"Server Started")
    logger.info(f"config type: {config_type}")

    #cache = create_cache(app_settings, app)

    # Access config variables as: app.config['DEBUG']
    # Register all api blueprints found in the application
    print (package_path)
    register_blueprints(app, package_name, package_path)

    return app
