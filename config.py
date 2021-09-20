import os
class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_GB")
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kev2214@localhost/tests'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SECRET_KEY = 'kev'

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USERNAME ='kevohronoh@gmail.com'
    MAIL_PASSWORD = 'alicerono2214'

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kev2214@localhost/tests'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kev2214@localhost/tests'
    DEBUG = True
    

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}