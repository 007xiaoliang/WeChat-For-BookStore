from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 用户表
class User(db.Model):
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    img_id = db.Column(db.String(50))
    regis_date = db.Column(db.DateTime, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)


# 角色表
class Role(db.Model):
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.INTEGER, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    persons = db.relationship('User', backref='role', lazy=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=False)


# 权限表
class Permission(db.Model):
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.INTEGER, primary_key=True)
    permission_name = db.Column(db.String(50), nullable=False)
    roles = db.relationship('Role', backref='permission', lazy=True)
