import os


base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = '123456'
    # 模板文件自动加载
    TEMPLATES_AUTO_RELOAD = True
    # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 邮件发送
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'chao__chao1@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'liangfei779108'
    # 文件上传
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')


# 开发环境配置
class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'product': ProductConfig,

    'default': DevelopConfig
}
