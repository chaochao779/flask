from .main import main
from .user import user

# 蓝本配置
CONFIG_BLUEPRINT = (
    # （蓝本, 前缀）
    (main, ''),
    (user, '/user'),
)


def register_blueprint(app):
    for blueprint, url_prefix in CONFIG_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
