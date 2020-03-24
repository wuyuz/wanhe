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


class Medicine(models.Model):
    """ 基础表 """

    __tablename__ = 'medicine'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(64))
    size = models.Column(models.String(64), nullable=True)
    taboo = models.Column(models.String(128), nullable=True)
    note = models.Column(models.String(255))

    def save(self):
        models.session.add(self)
        models.session.commit()


class Plan(models.Model):
    """ 包表 """

    __tablename__ = 'plans'
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(64))

