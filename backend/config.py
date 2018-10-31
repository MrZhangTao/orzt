import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "It is just a key")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/orzt")
    # 定义一个字典用于保存错误码以及错误信息
    errorDict = {
        "401": "Unauthorized Access!",
        "404": "Sorry, Not Found!!!!!"
    }

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
