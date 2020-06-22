"""
Global Configuration for Application
"""
import os

class BaseConfig:
    TESTING = os.getenv("TESTING")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    
class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DEV_URI", "sqlite:///site.db") # development
    DEBUG = True
    
class TestingConfig(BaseConfig):
    FLASK_ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URI", "sqlite:///test.db") # development
    
class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PRODUCTION_URI") # production. copy and paste postgres URI as backup once ready
    SECRET_KEY = "not_confirmed"