import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

class Config:
    # protects against modifying cookies and cross-site forgery attacks
    # import secrets; secrets.token_hex(16) to generate the token
    SECRET_KEY = config.get('SECRET_KEY')
    # with sqlite we can specify a relative path with /*3
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # will be created in our project directory
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')  # will be created in our project directory
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')
    APP_USERNAME = config.get('APP_USERNAME')
    APP_PASSWORD = config.get('APP_PASSWORD')
    PYTHONPATH = config.get('PYTHONPATH')

# class Config:
#     # protects against modifying cookies and cross-site forgery attacks
#     # import secrets; secrets.token_hex(16) to generate the token
#     SECRET_KEY = os.environ['SECRET_KEY']
#     # with sqlite we can specify a relative path with /*3
#     # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # will be created in our project directory
#     SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']  # will be created in our project directory
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ['EMAIL_USER']
#     MAIL_PASSWORD = os.environ['EMAIL_PASS']
#     APP_USERNAME = os.environ['APP_USERNAME']
#     APP_PASSWORD = os.environ['APP_PASSWORD']
#     PYTHONPATH = os.environ['PYTHONPATH']
#
#
