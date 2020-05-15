# coding: utf-8
from wanhe.ext import models
from werkzeug.security import check_password_hash, generate_password_hash


class User(models.Model):
    """ 用户配置 """
    __tablename__ = 'user'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    username = models.Column(models.String(64), unique=True)
    _s_password = models.Column(models.String(128))
    role = models.Column(models.SmallInteger, default=1)
    other = models.Column(models.String(32), default=None)
    @property
    def s_password(self):
        raise Exception("Error Action")

    @s_password.setter
    def s_password(self, value):
        self._s_password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self._s_password, password)

    def save(self):
        models.session.add(self)
        models.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class MedicineType(models.Model):
    __tablename__ = "medicinetype"
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(64))
    content = models.Column(models.Text, nullable=False)
    def save(self):
        models.session.add(self)
        models.session.commit()
    def delete(self):
        # 查询是否关联medicine
        try:
            models.session.delete(self)
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False
    def commit(self):
        try:
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False
    def validate_type(self, field):
        is_exist = Medicine.query.filter_by(mtid=field).all()
        if is_exist:
            return False
        return True
    def __repr__(self):
        return self.name

class Medicine(models.Model):
    """ 基础表 """

    __tablename__ = 'medicine'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(64))
    size = models.Column(models.String(64), nullable=True)
    taboo = models.Column(models.String(128), nullable=True)
    sale = models.Column(models.String(12),nullable=True)
    note = models.Column(models.String(255))
    mtid = models.Column(models.Integer, models.ForeignKey('medicinetype.id'))
    mtype = models.relationship("MedicineType", backref="medicinetypes")
    def save(self):
        models.session.add(self)
        models.session.commit()

    def delete(self):
        try:
            models.session.delete(self)
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False

    def commit(self):
        try:
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False
    def validate_plan(self, field):
        is_exist = PlanMedicine.query.filter_by(medicineid=field).all()
        if is_exist:
            return False
        return True



class Plan(models.Model):
    """ 方案表 """

    __tablename__ = 'plans'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(64))
    total_sale = models.Column(models.String(24))
    illness = models.Column(models.String(128))

    def save(self):
        models.session.add(self)
        models.session.commit()

    def delete(self):
        try:
            models.session.delete(self)
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False

    def commit(self):
        try:
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False

class PlanMedicine(models.Model):
    """ 方案组合表"""

    __tablename__ = 'plan_medicine'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    planid = models.Column(models.String(64))
    medicineid = models.Column(models.String(64))

    def save(self):
        models.session.add(self)
        models.session.commit()

    def delete(self):
        try:
            models.session.delete(self)
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False

    def commit(self):
        try:
            models.session.commit()
            return True
        except Exception as e:
            models.session.rollback()  # 事务
            return False
