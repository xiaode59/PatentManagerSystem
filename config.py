import os
from datetime import timedelta

class Config:
    '''基础配置'''
    DEBUG = True
    SECRET_KEY = 'lab_patent_secret_2025_demo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///patent_knowledge.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置（未来扩展）
    JWT_SECRET_KEY = 'jwt_lab_patent_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class DevelopmentConfig(Config):
    '''开发环境配置'''
    DEBUG = True

class ProductionConfig(Config):
    '''生产环境配置'''
    DEBUG = False