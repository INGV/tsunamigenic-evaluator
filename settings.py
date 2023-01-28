# -*- coding: utf-8 -*-
"""
    file: settings.py
    notes:  Configure Settings for application
"""

import os

class Config(object):
    """ Common config options """
    CACHE_DIR = os.getenv('CACHE_DIR') or './.cache'
    APPNAME = 'traveltime_Docker'
    SUPPORT_EMAIL = 'sergio.bruni@ingv.it'
    VERSION = '1.0.0'
    APPID = 'traveltime_Docker'
    SECRET_KEY = os.urandom(24)
    TESTING = False
    LOG_SEVERITY = 'INFO'

class DevelopmentConfig(Config):
    """ Dev environment config options """
    FLASK_ENV='development'
    DEBUG = True
    PROFILE = True
    LOG_SEVERITY = 'DEBUG'

class TestingConfig(Config):
    """ Testing environment config options """
    DEBUG = False
    STAGING = True
    TESTING = True
    LOG_SEVERITY = os.getenv('LOG_SEVERITY') or 'DEBUG'


class ProductionConfig(Config):
    """ Prod environment config options """
    FLASK_ENV = 'production'
    DEBUG = False
    STAGING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
