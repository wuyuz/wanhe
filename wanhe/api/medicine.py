from flask_restful import Resource, fields, marshal_with, reqparse, request
from flask import jsonify
from wanhe.utils.pagination import Pagination
from wanhe.model import Medicine, MedicineType
from sqlalchemy import exists
# 序列化
# 药品类型序列化
medicinetype_field = {
    "id":fields.Integer,
    "name":fields.String(),
    "content":fields.String
}

medicine_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'size': fields.String,
    'taboo': fields.String,
    'sale':fields.String,
    'note':fields.String,
    'mtid': fields.Integer,
    'mtype':fields.Nested(medicinetype_field)
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

single_medicinetype_fields = {
    "data": fields.Nested(medicinetype_field),
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
        id = request.args.get('id')
        # 单个id查询
        if id:
            obj = Medicine.query.filter_by(id=id).first()

            data = {
                "status": 200,
                "msg": 'OK',
                "data": obj,
            }
            return data

        else:
            query = request.args.get('query')
            if query:
                medicines = Medicine.query.filter(
                    Medicine.name.like("%"+query+"%") if query is not None else ""
                ).all()
            else:
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
            return jsonify({
                'code': 202,
                'msg': '新增失败'
            })
        return jsonify({
            'code': 200,
            'msg': '新增成功'
        })

    def delete(self):
        """
        删除实现函数
        :return:
        """
        id = request.args.get('id')
        # 单个id查询
        if id:
            obj = Medicine.query.filter_by(id=id).first()
            is_exist = obj.validate_plan(id)
            if is_exist:
                obj.delete()
                return jsonify({
                    'code': 200,
                    'msg': '删除成功'
                })
        return jsonify({
            'code': 202,
            'msg': '删除失败'
        })

    def put(self):
        id = request.json.get('id')
        obj = Medicine.query.filter_by(id=id).first()
        if not obj:
            return jsonify({
                'code': 203,
                'msg': "修改失败"
            })

        obj.name = request.json.get('name')
        obj.size = request.json.get('size')
        obj.taboo = request.json.get('taboo')
        obj.sale = request.json.get('sale')
        obj.note = request.json.get('note')
        obj.mtid = request.json.get('mtid')

        if obj.commit():
            return jsonify({
                'code': 200,
                'msg': "修改接口成功"
            })
        else:
            return jsonify({
                'code': 203,
                'msg': "修改接口失败"
            })


class MedicineTypeResource(Resource):
    @marshal_with(single_medicinetype_fields)
    def get(self):
        id = request.args.get('id')
        # 单个id查询
        if id:
            obj = MedicineType.query.filter_by(id=id).first()

            data = {
                "status": 200,
                "msg": 'OK',
                "data": obj,
            }
            return data

        else:
            query = request.args.get('query')
            if query:
                medicinesType = MedicineType.query.filter(
                    MedicineType.name.like("%" + query + "%") if query is not None else ""
                ).all()
            else:
                medicinesType = MedicineType.query.all()
            total = len(medicinesType)
            page = request.args.get('page')
            size = request.args.get('size')
            query = request.args.get('query')
            paginate = Pagination(int(request.args.get('page')), total, request.base_url, request.args.get('query'),
                                  int(request.args.get('size')))
            medicineTypeList = medicinesType[paginate.start:paginate.end]
            data = {
                "status": 200,
                "msg": 'OK',
                "data": medicineTypeList,
                "count": total,
                "next": paginate.next,
                "previous": paginate.prev,
            }
            return data

    def post(self):
        try:
            obj = MedicineType(**request.json)
            obj.save()
        except Exception as e:
            return jsonify({
                'code': 202,
                'msg': '新增药品类型失败'
            })
        return jsonify({
            'code': 200,
            'msg': '新增药品类型成功'
        })
    def delete(self):
        """
        删除实现函数
        :return:
        """
        id = request.args.get('id')
        # 单个id查询
        if id:
            obj = MedicineType.query.filter_by(id=id).first()
            # Medicine.query.filter_by(
            #     exists()
            # )
            is_exist = obj.validate_type(obj.id)
            if is_exist:
                obj.delete()
                return jsonify({
                    'code': 200,
                    'msg': '删除成功'
                })
        return jsonify({
            'code': 202,
            'msg': '删除失败'
        })

    def put(self):
        id = request.json.get('id')
        obj = MedicineType.query.filter_by(id=id).first()
        if not obj:
            return jsonify({
                'code': 203,
                'msg': "修改失败"
            })

        obj.name = request.json.get('name')
        obj.content = request.json.get('content')

        if obj.commit():
            return jsonify({
                'code': 200,
                'msg': "修改接口成功"
            })
        else:
            return jsonify({
                'code': 203,
                'msg': "修改接口失败"
            })
