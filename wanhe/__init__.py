# coding: utf-8
from flask import Flask
from wanhe.config import envs  # 加载配置文件
from wanhe.ext import init_ext  # 加载第三方配置库
from wanhe.api import init_api


def create_app():
    """
    初始化app，完成相应的配置
    :return: 返回app
    """
    app = Flask(__name__)
    app.config.from_object(envs.get('develop') or 'develop')  # 选择运行环境
    init_ext(app)  # 初始化第三方库
    init_api(app)  # 注册api
    return app
