from flask_restful import Resource, fields, marshal_with, reqparse, request, marshal
from flask import jsonify
import json
from wanhe.utils.pagination import Pagination
from wanhe.model import Plan, PlanMedicine, Medicine

# 序列化
medicine_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'total_sale': fields.String,
    'illness': fields.String,
    'detail': fields.String,
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


class PlanResource(Resource):
    def get(self):
        id = request.args.get('id')
        full = request.args.get('full')
        if full:
            val = []
            all = Medicine.query.all()
            for i in all:
                val.append({'value': i.id, 'label': i.name})
            data = {
                "status": 200,
                "msg": 'OK',
                "data": val,
            }
            return jsonify(data)

        # 单个id查询
        if id:
            obj = Plan.query.filter_by(id=id).first()
            plans_all = PlanMedicine.query.filter_by(planid=obj.id).all()
            msg = []
            for i in plans_all:
                msg.append(i.medicineid)

            obj.detail = json.dumps(msg)
            data = {
                "status": 200,
                "msg": 'OK',
                "data": obj,
            }
            return marshal(data, single_fields)


        else:
            plans = Plan.query.all()
            total = len(plans)
            paginate = Pagination(int(request.args.get('page')), total, request.base_url, request.args.get('query'),
                                  int(request.args.get('size')))
            plan_list = plans[paginate.start:paginate.end]
            plans_all = PlanMedicine.query.all()

            for plan in plan_list:
                msg = []
                for i in plans_all:
                    if str(plan.id) == i.planid:
                        msg.append(i.medicineid)
                plan.detail = ','.join(list(map(lambda x: x.name, Medicine.query.filter(Medicine.id.in_(msg)))))
            data = {
                "status": 200,
                "msg": 'OK',
                "data": plan_list,
                "count": total,
                "next": paginate.next,
                "previous": paginate.prev,
            }
            return marshal(data, single_fields)

    def post(self):
        try:
            obj = Plan(name=request.json.get("name"), total_sale=request.json.get('total_sale'),
                       illness=request.json.get('illness'))
            val = request.json.get('value')
            obj.save()
            for i in val:
                p_m = PlanMedicine(planid=obj.id, medicineid=i)
                p_m.save()

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
            obj = Plan.query.filter_by(id=id).first()
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
        obj = Plan.query.filter_by(id=id).first()
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
