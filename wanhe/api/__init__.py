from flask_restful import Api
from wanhe.api.auth import UserResource
from wanhe.api.medicine import MedicineResource

api = Api()

def init_api(app):
    """
    初始化注册api
    :param app:
    :return:
    """
    api.init_app(app)


api.add_resource(UserResource, '/api/v1/login/')
api.add_resource(MedicineResource, '/api/v1/medicine/')
