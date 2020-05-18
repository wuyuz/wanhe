# coding: utf-8
from flask import request, jsonify
from flask_restful import Resource
# from werkzeug.security import generate_password_hash

from wanhe.utils.jwt import Jwt
from wanhe.model import User
from wanhe.config import Config


class UserResource(Resource):
    """ 用户登陆实现类 """

    def get(self):

        menusList = [
            {'id': 1, 'title': '检索', 'menu_icon': 'el-icon-search', 'children': [{
                'id': 4, 'title': '检索平台', 'url': 'server', 'icon': 'el-icon-location-outline'
            }, ]},
            {'id': 2, 'title': '药品', 'menu_icon': 'el-icon-postcard', 'children': [{
                'id': 5, 'title': '药品信息', 'url': 'medicine', 'icon': 'el-icon-location-outline'
            }, {
                'id': 7, 'title': '药品类型', 'url': 'medicinetype', 'icon': 'el-icon-paperclip'
            }]},
            {'id': 3, 'title': '方案', 'menu_icon': 'el-icon-first-aid-kit', 'children': [{
                'id': 6, 'title': '方案信息', 'url': 'plans', 'icon': 'el-icon-location-outline'
            }, ]},
        ]
        # pwd = generate_password_hash("123456")
        # obj = User(username="root",_s_password=pwd)
        # obj.save()
        return jsonify({
            'code': 200,
            'data': menusList,
        })

    def post(self):
        """
        登陆逻辑实现
        :return:
        """
        name = request.json.get('username')
        password = request.json.get('password')
        find_one = User.query.filter(User.username.__eq__(name)).first()
        print(find_one,find_one.check_password(password))
        if find_one and find_one.check_password(password):
            token = Jwt.encode({'username': name}, Config.SIGN)
            return jsonify({
                'code': 200,
                'username': name,
                'token': token.decode('utf-8')
            })
        else:
            return jsonify({
                'code': 202,
                'username': name
            })
