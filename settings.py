import os

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = bool(int(os.getenv('DEBUG', 1)))

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL')
