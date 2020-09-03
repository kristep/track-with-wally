import os


class BaseConfig(object):
    DEBUG = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/db.sqlite'
    SECRET_KEY = "secret123"


class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://kzstqwqwlpavnh:cb8c327321d6364375a3a27f43c6a0d617a5165b786c3de600271adac1f4fe31@ec2-3-223-9-166.compute-1.amazonaws.com:5432/d8gjmdanvqjid8'


class HerokuConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
