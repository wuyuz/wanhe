# coding: utf-8

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

models = SQLAlchemy()  # 创建一个models对象
migrate = Migrate()


# 导入的第三方库,整合
def init_ext(app):
    models.init_app(app=app)  # models需要知道绑定的app，这里提供了懒加载的初始化配置app的方式
    migrate.init_app(app, models)  # 初始化迁移配置
    CORS(app)
