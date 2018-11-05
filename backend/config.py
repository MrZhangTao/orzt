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
    #数据库配置
    CHOSQL = "mysql"
    DRIVER = "+pymysql"
    USERNAME = "root"
    PASSWORD = "password"
    HOSTNAME = "localhost" # "127.0.0.1"
    PORT = "3306"
    DATABASE = "orzt"
    dburi = "{}{}://{}:{}@{}:{}/{}".format(CHOSQL, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", dburi)
    # 定义一个字典用于保存错误码以及错误信息
    errorDict = {
        "401": "Unauthorized Access!",
        "404": "Sorry, Not Found!!!!!"
    }

class ProductConfig(Config):
    DEBUG = False
    ENV = "Product"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PRO_DATABASE_URL"
    )

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
