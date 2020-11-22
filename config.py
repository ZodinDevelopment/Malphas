import os
import secrets
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['dmgarrett72@protonmail.com']
    ITEMS_PER_PAGE = 10
    MEDIA_PER_PAGE = 4
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    IMAGE_EXTENSIONS = ['jpg', 'gif', 'png']
    VIDEO_EXTENSIONS = ['mp4', 'mov', 'webm']
    AUDIO_EXTENSIONS = ['wav', 'mp3', 'ogg']
    INDEX_CONTENT = os.path.join(basedir, 'index.txt')
        
