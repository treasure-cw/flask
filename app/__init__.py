# -*- coding:utf-8 -*-
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

'''
创建Flask对象函数
'''


def create_app():
    app = Flask(__name__)
    app.jinja_env.filters['zip'] = zip
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = '123456'
    # ip:服务器（数据库）地址
    # pwd:数据库密码
    # usr:数据库用户名
    ip = "47.98.235.106"
    pwd = "123456"
    usr = "root"
    # 连接数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{usr}:{pwd}@{ip}:3306/TechSystem'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 初始化SQLAlchemy对象
    # 初始化bootstrap对象
    # 初始化login_manager对象
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    # 导入蓝图
    from .auth import auth as auth_blueprint
    from .systemadmin import systemadmin as systemadmin_blueprint
    from .eduadmin import eduadmin as eduadmin_blueprint
    from .teacher import teacher as teacher_blueprint
    from .student import student as student_blueprint
    # 把蓝图注册到flask对象上
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(systemadmin_blueprint)
    app.register_blueprint(eduadmin_blueprint)
    app.register_blueprint(teacher_blueprint)
    app.register_blueprint(student_blueprint)

    # 判断当前路由
    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path
    # 返回flask对象
    return app
