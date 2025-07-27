import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:hyxtas-0Cazbi-suxjoq@localhost:3306/astock')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
