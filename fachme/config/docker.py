import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://fachme:fachme@db:3306/fachme'
)
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
SESSION_TYPE = 'filesystem'
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
AUTOCOMPLETE_NAMESPACE = 'character_autocomplete'
SQLALCHEMY_TRACK_MODIFICATIONS = False
