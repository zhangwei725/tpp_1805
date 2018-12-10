def get_db_uri(database: dict):
    engine = database.get('ENGINE') or 'mysql'
    user = database.get('USER') or 'root'
    password = database.get('PASSWORD') or 'root'
    driver = database.get('DRIVER') or 'pymysql'
    host = database.get('HOST') or '127.0.0.1'
    port = database.get('PORT') or '3306'
    name = database.get('NAME')
    charset = database.get('CHARSET') or 'utf8'
    return f"{engine}+{driver}://{user}:{password}@{host}:{port}/{name}?charset={charset}"


# 开发环境
class DeveloperConfig:
    DEBUG = True
    SECRET_KEY = '123456'
    database = {
        'ENGINE': 'mysql',
    }
    # 输出sql语句
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = get_db_uri(database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 生成数据连接 dialect+driver://username:password@host:port/database

# 生产环境
class ProductConfig:
    DEBUG = False
    SECRET_KEY = '4ce01aa944434ff4880b29b0992ee846'
    database = {
        'ENGINE': 'mysql',
        'HOST': '112.74.42.138',
        'PORT': '3306',
        'NAME': 'film',
    }
    # 生成环境小设置连接池的数量
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_DATABASE_URI = get_db_uri(database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


environment = {
    'default': DeveloperConfig,
    'dev': DeveloperConfig,
    'product': ProductConfig
}
