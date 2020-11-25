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
    INDEX_CONTENT = '''
        This web application features a fully functional database engine and 
    is built with the MVC development approach (Model-View-Controller) using 
    the powerful high-level programming language Python. Python's Flask Web 
    Framework lets you build robust, interactive, enterprise level web sites
    with it's modular brick-and-mortar design philosophy. 
        For instance, this website implements a user authentication system, 
    private messages to other users, and even allows users to post and follow
    others. I build websites around its data models. These models are users,
    customers, products, posts, messages, transactions, anythiing at all.
    URL's are routed to functions that make queries and entries into the 
    database so that dynamic content can be rendered and presented to the 
    user in the form of an interactive website. 
        The actual layout and appearance of the webpage is arbitrary here
    and can be customized or completed redesigned. Not only is the front end
    customizable, but the application's capabilities and purpose can be 
    easily expanded and changed. 
    '''
        
