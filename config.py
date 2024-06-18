import os

class Config:
    
    SECRET_KEY = "SUPER-SECRET-KEY"
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:root@localhost/mysql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')