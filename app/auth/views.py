from flask import render_template, redirect, url_for
from . import auth
from .forms import LoginForm
from ..models import *
from .. import db
from flask_login import login_user, logout_user, current_user

'''
默认界面：
如果由用户登录，那么退出登录
如果没有，重定向到登录界面
'''


@auth.route('/')
def index():
    # 如果当前用户为空则登录
    if current_user.get_id() is None:
        return redirect(url_for('auth.login'))
    # 否则退出当前用户的登录状态，重新登录
    else:
        return redirect(url_for('auth.logout'))


'''
登录业务：
用户输入账号，密码进行登录；
函数判断用户类型，系统管理员8位，教务员9位，教师10位，学生12位；
函数判断数据库中是否存在该用户；
判断后重定向到各自初始界面；
'''


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # form:登录表单
    form = LoginForm()
    # 判断表单是否提交
    if form.validate_on_submit():
        # 用户id长度是8，判断为系统管理员
        if len(form.userid.data) == 8:
            # 查找id,password为表单提交内容的用户
            user = Sysadmin.query.filter_by(id=form.userid.data, password=form.password.data).first()
            # 如果用户存在，登录该用户（cookies保存），重定向到系统管理员界面
            if user is not None:
                login_user(user)
                return redirect(url_for('systemadmin.sys', id=form.userid.data))
        # 用户id长度是9，判断为教务员
        elif len(form.userid.data) == 9:
            # 查找id,password为表单提交内容的用户
            user = Eduadmin.query.filter_by(id=form.userid.data, password=form.password.data).first()
            # 如果用户存在，登录该用户（cookies保存），重定向到教务员界面
            if user is not None:
                login_user(user)
                return redirect(url_for('eduadmin.edu', id=form.userid.data))
        # 用户id长度是10，判断为教师
        elif len(form.userid.data) == 10:
            # 查找id,password为表单提交内容的用户
            user = Teacher.query.filter_by(id=form.userid.data, password=form.password.data).first()
            # 如果用户存在，登录该用户（cookies保存），重定向到教师界面
            if user is not None:
                login_user(user)
                return redirect(url_for('teacher.tea', id=form.userid.data))
        # 用户id长度是12，判断为学生
        elif len(form.userid.data) == 12:
            # 查找id,password为表单提交内容的用户
            user = Student.query.filter_by(id=form.userid.data, password=form.password.data).first()
            # 如果用户存在，登录该用户（cookies保存），重定向到学生界面
            if user is not None:
                login_user(user)
                return redirect(url_for('student.stu', id=form.userid.data))
        else:
            pass
    return render_template('login.html', title='登录', form=form)


'''
退出登录业务：
退出当前用户；
重定向到登录界面；
'''


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
