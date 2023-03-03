import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.jpeg']
    MAX_CONTENT_LENGTH = 2048 * 2048
    UPLOAD_PATH = 'static/uploads/'

    MAIL_SERVER = 'smtp.hostinger.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 0
    MAIL_USERNAME = 'eeb2@t-o.ie'
    MAIL_PASSWORD = 'Thisisthepassword1!'
    # TODO: Change password
    ADMINS = ['eeb2@t-o.ie']
