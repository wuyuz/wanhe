from flask_restful import Api
from wanhe.api.auth import UserResource
from wanhe.api.medicine import MedicineResource, MedicineTypeResource
from wanhe.api.plans import PlanResource
from wanhe.api.search import Searchquery

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
api.add_resource(MedicineTypeResource, '/api/v1/medicinetype/')

api.add_resource(PlanResource, '/api/v1/plans/')
api.add_resource(Searchquery, '/api/v1/search/')
