# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, request
from . import systemadmin
from ..models import *
from .forms import *
from flask_login import login_required, current_user
from os import path
from werkzeug.utils import secure_filename

'''
删除教务员业务：
id:要删除教务员的id；
myid:当前登录用户的id；
'''


@systemadmin.route('/deledu/<string:id>/<string:myid>')
def deleteedu(id, myid):
    me = Eduadmin.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
删除系所业务：
id:要删除系所的id；
myid:当前登录用户的id；
'''


@systemadmin.route('/deldepart/<string:id>/<string:myid>')
def deletedepart(id, myid):
    me = Department.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
删除专业业务：
id:要删除专业的id；
myid:当前登录用户的id；
'''


@systemadmin.route('/deletemaj/<string:id>/<string:myid>')
def deletemaj(id, myid):
    me = Major.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
删除课程类别业务：
id:要删除课程类别的id；
myid:当前登录用户的id；
'''


@systemadmin.route('/deletetype/<string:id>/<string:myid>')
def deletetype(id, myid):
    me = Coursetype.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
删除班级业务：
id:要删除班级的id；
myid:当前登录用户的id；
'''


@systemadmin.route('/deleteclass/<string:id>/<string:myid>')
def deleteclass(id, myid):
    me = Class.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
修改教务员信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的教务员，按表单修改；
重定向会系统管理员主页；
'''


@systemadmin.route('/modifyedu/<string:myid>', methods=['POST'])
def modifyedu(myid):
    id = request.form['fid']
    me = Eduadmin.query.filter_by(id=id).first()
    me.name = request.form['fname']
    me.password = request.form['fpassword']
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
修改系所信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的系所，按表单修改；
重定向会系统管理员主页；
'''


@systemadmin.route('/modifydepart/<string:myid>', methods=['POST'])
def modifydepart(myid):
    id = request.form['fid']
    me = Department.query.filter_by(id=id).first()
    me.name = request.form['fname']
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
修改专业信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的专业，按表单修改；
重定向会系统管理员主页；
'''


@systemadmin.route('/modifymaj/<string:myid>', methods=['POST'])
def modifymaj(myid):
    id = request.form['fid']
    me = Major.query.filter_by(id=id).first()
    me.departmentid = request.form['fs']
    me.name = request.form['fname']
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
修改课程类别信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的课程类别，按表单修改；
重定向会系统管理员主页；
'''


@systemadmin.route('/modifytype/<string:myid>', methods=['POST'])
def modifytype(myid):
    id = request.form['fid']
    me = Coursetype.query.filter_by(id=id).first()
    me.name = request.form['fname']
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
修改班级信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的班级，按表单修改；
重定向会系统管理员主页；
'''


@systemadmin.route('/modifyclass/<string:myid>', methods=['POST'])
def modifyclass(myid):
    id = request.form['fid']
    me = Class.query.filter_by(id=id).first()
    me.majorid = request.form['fs']
    me.name = request.form['fname']
    me.startyear = request.form['fdate']
    db.session.commit()
    return redirect(url_for('systemadmin.sys', id=myid))


'''
系统管理员主界面：
先行登录验证通过才能访问；
参数id为系统管理员账号；
'''


@systemadmin.route('/sys/<string:id>', methods=['GET', 'POST'])
@login_required
def sys(id):
    # myself:当前登录用户对象
    myself = Sysadmin.query.filter_by(id=id).first()
    # form1:添加教务员表单
    # form2:添加系所表单
    # form3:添加专业表单
    # form4:添加课程类别表单
    # form5:添加班级表单
    form1 = AddEduadminForm()
    form2 = AddDepartmentForm()
    form3 = AddMajorForm()
    form4 = AddCoursetypeForm()
    form5 = AddClassForm()
    # eduadmin[]:数据库内所有教务员对象列表
    # department[]:数据库内所有系所对象列表
    # major[]:数据库内所有专业对象列表
    # coursetype[]:数据库内所有课程类别对象列表
    # classs[]:数据库内所有班级对象列表
    eduadmin = Eduadmin.query.all()
    department = Department.query.all()
    major = Major.query.all()
    coursetype = Coursetype.query.all()
    classs = Class.query.all()
    # 为表单的选择框动态添加信息
    form3.departmentname.choices += [(r.id, r.name) for r in department]
    form5.majorname.choices += [(r.id, r.name) for r in major]
    # x:标识,表示数据库是否发生可改变，default 0
    x = 0
    # 如果添加教务员表单提交
    if form1.submit1.data and form1.validate():
        # 如果教务员对象列表不为空
        # 教务员id为最后一名教务员的id+1
        if eduadmin:
            idd = str(int(eduadmin[-1].id) + 1)
        # 否则要添加的教务员就是第一名教务员
        # 初始化学生id为100000001
        else:
            idd = '100000001'
        # 添加教务员进入数据库
        me = Eduadmin(id=idd, name=form1.name.data, password=form1.password.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加系所表单提交
    elif form2.submit2.data and form2.validate():
        # 如果系所对象列表不为空
        # 系所id为最后一个系所的id+1
        if department:
            idd = str(int(department[-1].id) + 1)
        # 否则要添加的系所就是第一个系所
        # 初始化学生id为100001
        else:
            idd = '100001'
        # 添加系所进入数据库
        me = Department(id=idd, name=form2.name.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加专业表单提交
    elif form3.submit3.data and form3.validate():
        # 如果专业对象列表不为空
        # 专业id为最后一个专业的id+1
        if major:
            idd = str(int(major[-1].id) + 1)
        # 否则要添加的专业就是第一个系所
        # 初始化专业id为1000001
        else:
            idd = '1000001'
        # 添加专业进入数据库
        me = Major(id=idd, departmentid=form3.departmentname.data, name=form3.name.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加课程类别表单提交
    elif form4.submit4.data and form4.validate():
        # 如果课程类别对象列表不为空
        # 课程类别id为最后一个课程类别的id+1
        if coursetype:
            idd = str(int(coursetype[-1].id) + 1)
        # 否则要添加的课程类别就是第一个系所
        # 初始化课程类别id为0
        else:
            idd = '0'
        # 添加课程类别进入数据库
        me = Coursetype(id=idd, name=form4.name.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加班级类别表单提交
    elif form5.submit5.data and form4.validate():
        # 如果班级对象列表不为空
        # 班级id为最后一个班级的id+1
        if classs:
            idd = str(int(classs[-1].id) + 1)
        # 否则要添加的班级就是第一个系所
        # 初始化班级id为0
        else:
            idd = '10000001'
        # 添加班级进入数据库
        me = Class(id=idd, majorid=form5.majorname.data, name=form5.name.data, startyear=form5.startyear.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果标识为一，更新各列表
    if x == 1:
        eduadmin = Eduadmin.query.all()
        department = Department.query.all()
        major = Major.query.all()
        coursetype = Coursetype.query.all()
        classs = Class.query.all()
    # 进入模板，传递参数
    return render_template('sysadmin.html',
                           myself=myself,
                           Dep=Department, Maj=Major,
                           eduadmin=eduadmin, department=department,
                           coursetype=coursetype, major=major, classs=classs,
                           form1=form1, form2=form2, form3=form3, form4=form4, form5=form5)


'''
修改密码业务：
需要用户处于登录状态；
判断用户类型；
找到当前用户，修改密码；
退出当前登录用户
'''


@systemadmin.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    # form:重置密码表单
    form = ChangePassword()
    # 如果表单提交
    if form.submit5.data and form.validate():
        # 如果当前用户是系统管理员
        if len(current_user.get_id()) == 8:
            me = Sysadmin.query.filter_by(id=current_user.get_id()).first()
            me.password = form.password.data
            db.session.commit()
        # 如果当前用户是教务员
        elif len(current_user.get_id()) == 9:
            me = Eduadmin.query.filter_by(id=current_user.get_id()).first()
            me.password = form.password.data
            db.session.commit()
        # 如果当前用户是教师
        elif len(current_user.get_id()) == 10:
            me = Teacher.query.filter_by(id=current_user.get_id()).first()
            me.password = form.password.data
            db.session.commit()
        # 如果当前用户是学生
        elif len(current_user.get_id()) == 12:
            me = Student.query.filter_by(id=current_user.get_id()).first()
            me.password = form.password.data
            db.session.commit()
        # 重定向到等出界面
        return redirect(url_for('auth.logout'))
    return render_template('changepwd.html', form=form)


'''
404 not found
'''


@systemadmin.errorhandler(404)
def page_not_found():
    return "对不起，您访问的页面不存在"
