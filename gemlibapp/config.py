import os

class Config:
    # protects against modifying cookies and cross-site forgery attacks
    # import secrets; secrets.token_hex(16) to generate the token
    # SECRET_KEY = '9eeb7bda6af792d5a0313ad8e481b7a3'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # with sqlite we can specify a relative path with /*3
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # will be created in our project directoryapp.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # will be created in our project directory
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

