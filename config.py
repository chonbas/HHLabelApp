# -----------------------------------------------------------
# File: config.py
# Description:
# File to encapsulate different configurations as objects to be 
# used by the application.
# Contains primary Config class, as well as DevelopmentConfig and 
# ProductionConfig subclasses.
#
# Usage:
# When app is initalized by Flask, using app/__init__.py,
# one specifies:  app = create_app('default')
# the specific configuration desired is passed in as an argument
# to the constructor, and it pulls the configuration from here.
# -----------------------------------------------------------


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Main Configauration class 
# Development config and production config
# Inherit from this primary class.
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super!DUP3R!Hard_to_Guess+String'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    RELOADER = True

    @staticmethod
    def init_app(app):
        pass
    

# DevelopmentConfig
# Specifies sqlite uri for use in DevelopmentConfig
#
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


# ProductionConfig
# First, tries to pull DATABASE_URL from  OS environment variables
# In production, this variable is specified using
# (in Debian) export DATABASE_URL=mysql:/// etc
# If environemnt variable not specified, app defaults to sqlite
class ProductionConfig(Config):
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,

    'default' : ProductionConfig
}
