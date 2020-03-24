from flask_restful import Resource, fields, marshal_with, reqparse, request
from flask import jsonify
from wanhe.utils.pagination import Pagination
from wanhe.model import Medicine

# 序列化
medicine_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'size': fields.String,
    'taboo': fields.String
}

# 嵌套数据序列化
single_fields = {
    "data": fields.Nested(medicine_fields),
    "status": fields.Integer,
    "msg": fields.String,
    "previous": fields.String,
    "next": fields.String,
    "count": fields.Integer,
}

query = reqparse.RequestParser()


class MedicineResource(Resource):

    @marshal_with(single_fields)
    def get(self):
        medicines = Medicine.query.all()
        total = len(medicines)
        paginate = Pagination(int(request.args.get('page')), total, request.base_url, request.args.get('query'),
                              int(request.args.get('size')))
        medicineList = medicines[paginate.start:paginate.end]

        data = {
            "status": 200,
            "msg": 'OK',
            "data": medicineList,
            "count": total,
            "next": paginate.next,
            "previous": paginate.prev,
        }
        return data

    def post(self):
        try:
            obj = Medicine(**request.json)
            obj.save()
        except Exception as e:
            print(e)
            return jsonify({'data': {
                'code': 202,
                'msg':'新增失败'
            }})
        return jsonify({'data': {
            'code': 200,
            'msg':'新增成功'
        }})
