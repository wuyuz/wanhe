#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# Author Xu Junkai
# coding=utf-8
# @Time    : 2020/5/15 11:16
# @Site    :
# @File    : search.py
# @Software: PyCharm
"""
import six
from flask_restful import Resource,fields,request,reqparse,marshal_with
from flask_restful.fields import MarshallingException

from wanhe.model import Plan, PlanMedicine, Medicine


class FmtIllness(fields.String):
    def format(self, value):
        query = request.args.get('query')
        count = value.count(query)
        value = value.replace(query,'<strong style="color:red">'+query+'</strong>',count)
        try:
            return six.text_type(value)
        except ValueError as ve:
            raise MarshallingException(ve)



class MedicineDetial(fields.String):
    def format(self, value):
        planns_all = PlanMedicine.query.filter_by(planid=value).all()
        fmt_value = ""
        for p in planns_all:
            medicine_name = Medicine.query.filter_by(id=p.medicineid).first().name
            fmt_value += "%s "%medicine_name
        try:
            return six.text_type(fmt_value)
        except ValueError as ve:
            raise MarshallingException(ve)

plans = {
    "id":fields.Integer,
    "name":fields.String,
    "total_sale":fields.String,
    "illness":FmtIllness,
    "detail":MedicineDetial(attribute="id"),
}

plan_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(plans),
}

class Searchquery(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("query", type=str)

    @marshal_with(plan_fields)
    def get(self):
        args = self.parser.parse_args()
        query = args.query
        all_symptom = Plan.query.filter(
            Plan.illness.like("%"+query+"%") if query is not None else ""
        ).all()
        data = {
            "status":200,
            "msg":"OK",
            "data":all_symptom
        }
        return data
