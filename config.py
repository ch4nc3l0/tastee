import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "a32sd156as"
    SQLALCHEMY_DATABASE_URI = os.environ['postgres://xoouzbxomnkewv:cda6adaed150127e02ff3fd307dbcbf26da99fc512809e0bc2ae5d8a63c8ec68@ec2-50-17-193-83.compute-1.amazonaws.com:5432/dfac869n1u1id']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class TestingConfig(Config):
    TESTING = False