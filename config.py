import os
from datetime import timedelta

class Config:
    # Secret key for session manangement and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///task_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)