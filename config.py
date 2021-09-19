import os
class Config:
    '''
    General configuration parent class
    '''
 
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kev2214@localhost/exhibitpitch'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SECRET_KEY = 'kev'

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}