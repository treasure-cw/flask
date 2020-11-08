# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, request
from . import eduadmin
from .forms import *
from ..models import *
from flask_login import login_required, current_user
from ..models import db

'''
删除学生业务：
id:要删除学生的id；
myid:当前登录用户的id；
'''


@eduadmin.route('/deletestu/<string:id>/<string:myid>')
def deletestu(id, myid):
    me = Student.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('eduadmin.edu', id=myid))


'''
删除教师业务：
id:要删除教师的id；
myid:当前登录用户的id；
'''


@eduadmin.route('/deletetea/<string:id>/<string:myid>')
def deletetea(id, myid):
    me = Teacher.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('eduadmin.edu', id=myid))


'''
删除课程业务：
id:要删除课程的id；
myid:当前登录用户的id；
'''


@eduadmin.route('/deletecou/<string:id>/<string:myid>')
def deletecou(id, myid):
    me = Course.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('eduadmin.edu', id=myid))


'''
删除排课业务：
id1:要删除排课的id；
id2:要删除排课的课程号；
myid:当前登录用户的id；
'''


@eduadmin.route('/deletecoup/<string:id1>/<string:id2>/<string:myid>')
def deletecoup(id1, id2, myid):
    me = Courseplan.query.filter_by(id=id1, classid=id2).first()
    db.session.delete(me)
    db.session.commit()
    return redirect(url_for('eduadmin.edu', id=myid))


'''
修改学生信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的学生，按表单修改；
重定向会教务员主页；
'''


@eduadmin.route('/modifystu/<string:myid>', methods=['POST'])
def modifystu(myid):
    id = request.form['fid']
    # me:要修改的学生对象
    me = Student.query.filter_by(id=id).first()
    # 按表单内容进行修改
    me.sex = request.form['fsex']
    me.brithday = request.form['fb']
    me.classid = request.form['fs']
    me.name = request.form['fname']
    me.password = request.form['fpassword']
    # 提交
    db.session.commit()
    # 重定向
    return redirect(url_for('eduadmin.edu', id=myid))


'''
修改教师信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的教师，按表单修改；
重定向会教务员主页；
'''


@eduadmin.route('/modifytea/<string:myid>', methods=['POST'])
def modifytea(myid):
    id = request.form['fid']
    # me:要修改的教师对象
    me = Teacher.query.filter_by(id=id).first()
    # 按表单内容进行修改
    me.departmentid = request.form['fs']
    me.name = request.form['fname']
    me.password = request.form['fpassword']
    # 提交
    db.session.commit()
    # 重定向
    return redirect(url_for('eduadmin.edu', id=myid))


'''
修改课程信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的课程，按表单修改；
重定向会教务员主页；
'''


@eduadmin.route('/modifycou/<string:myid>', methods=['POST'])
def modifycou(myid):
    id = request.form['fid']
    # me:要修改的课程对象
    me = Course.query.filter_by(id=id).first()
    # 按表单内容进行修改
    me.tag = request.form['fs']
    me.studyhour = request.form['fsh']
    me.name = request.form['fname']
    me.studyscore = request.form['fss']
    # 提交
    db.session.commit()
    # 重定向
    return redirect(url_for('eduadmin.edu', id=myid))


'''
修改教师信息业务：
myid:当前登录用户的id；
接收表单post来的数据；
找到要修改的排课，按表单修改；
重定向会教务员主页；
'''


@eduadmin.route('/modifycoup/<string:id>/<string:myid>', methods=['POST'])
def modifycoup(id, myid):
    idd = request.form['fid']
    me = Courseplan.query.filter_by(id=idd, classid=id).first()
    me.courseid = request.form['fs1']
    me.teacherid = request.form['fs2']
    me.classid = request.form['fs3']
    me.seq = request.form['fseq']
    me.num = int(request.form['fnum'])
    me.semester = request.form['fsem']
    db.session.commit()
    return redirect(url_for('eduadmin.edu', id=myid))


'''
教务员主界面：
先行登录验证通过才能访问；
参数id为教务员账号；
'''


@eduadmin.route('/edu/<string:id>', methods=['GET', 'POST'])
@login_required
def edu(id):
    # myself:当前登录用户对象
    myself = Eduadmin.query.filter_by(id=id).first()
    # form1:添加学生表单
    # form2:添加教师表单
    # form3:添加课程表单
    # form4:添加排课表单
    form1 = AddStudentForm()
    form2 = AddTeacherForm()
    form3 = AddCourseForm()
    form4 = AddCourseplanForm()
    # student[]:数据库内所有学生对象列表
    # teacher[]:数据库内所有教师对象列表
    # course[]:数据库内所有课程对象列表
    # courseplan[]:数据库内所有排课对象列表
    # classs[]:数据库内所有班级对象列表
    # department[]:数据库内所有系所对象列表
    # coursetype[]:数据库内所有课程类别对象列表
    student = Student.query.all()
    teacher = Teacher.query.all()
    course = Course.query.all()
    courseplan = Courseplan.query.all()
    classs = Class.query.all()
    department = Department.query.all()
    coursetype = Coursetype.query.all()
    # 为表单的选择框动态添加信息
    form1.classname.choices += [(r.id, r.name) for r in classs]
    form2.departmentname.choices += [(r.id, r.name) for r in department]
    form3.typename.choices += [(r.id, r.name) for r in coursetype]
    form4.coursename.choices += [(r.id, r.name) for r in course]
    form4.classname.choices = form1.classname.choices
    form4.teachername.choices += [(r.id, r.name) for r in teacher]
    # x:标识,表示数据库是否发生可改变，default 0
    x = 0
    # 如果添加学生表单提交
    if form1.submit1.data and form1.validate():
        # 如果学生对象列表不为空
        # 学生id为最后一名学生的id+1
        if student:
            idd = str(int(student[-1].id) + 1)
        # 否则要添加的学生就是第一名学生
        # 初始化学生id为100000000001
        else:
            idd = '100000000001'
        # 添加学生进入数据库
        me = Student(id=idd, sex=form1.sex.data,
                     brithday=form1.birthday.data,
                     classid=form1.classname.data,
                     name=form1.name.data,
                     password=form1.password.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加教师表单提交
    elif form2.submit2.data and form2.validate():
        # 如果教师对象列表不为空
        # 教师id为最后一名教师的id+1
        if teacher:
            idd = str(int(teacher[-1].id) + 1)
        # 否则要添加的教师就是第一名教师
        # 初始化教师id为1000000001
        else:
            idd = '1000000001'
        # 添加教师进入数据库
        me = Teacher(id=idd,
                     departmentid=form2.departmentname.data,
                     name=form2.name.data,
                     password=form2.password.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加课程表单提交
    elif form3.submit3.data and form3.validate():
        # 如果课程对象列表不为空
        # 课程id为最后一名课程的id+1
        if course:
            idd = str(int(course[-1].id) + 1)
        # 否则要添加的课程就是第一名课程
        # 初始化课程id为10000001
        else:
            idd = '10000001'
        # 添加课程进入数据库
        me = Course(id=idd, tag=form3.typename.data,
                    studyhour=form3.studyhour.data,
                    studyscore=form3.studyscore.data,
                    name=form1.name.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果添加排课计划表单提交
    elif form4.submit4.data and form4.validate():
        # temp:同一时间，统一班级，统一教师所上课的id
        temp = Courseplan.query.filter_by(courseid=form4.coursename.data, seq=form4.seq.data,
                                          teacherid=form4.teachername.data).first()
        # 如果temp存在，说明该课程排课已经存在
        # primary key(classid,id)
        # 即表面操作为为排课增加可选班级
        # 所以排课id就是temp的id
        if temp:
            idd = temp.id
        # 否则
        else:
            # 如果排课对象列表不为空
            # 排课id为最后一名排课计划的id+1
            if courseplan:
                idd = str(int(courseplan[-1].id) + 1)
            # 否则要添加的排课计划就是第一条排课计划
            # 初始化排课id为100000000001
            else:
                idd = '100000000001'
        # 添加排课进入数据库
        me = Courseplan(id=idd, courseid=form4.coursename.data,
                        seq=form4.seq.data,
                        teacherid=form4.teachername.data,
                        num=form4.num.data,
                        semester=form4.semester.data,
                        classid=form4.classname.data)
        db.session.add(me)
        db.session.commit()
        # 标识置为1
        x = 1
    # 如果标识为一，更新各列表
    if x == 1:
        student = Student.query.all()
        teacher = Teacher.query.all()
        course = Course.query.all()
        courseplan = Courseplan.query.all()
        classs = Class.query.all()
        department = Department.query.all()
        coursetype = Coursetype.query.all()
    form4.coursename.choices = []
    form4.coursename.choices += [(r.id, r.name) for r in course]
    form4.teachername.choices = []
    form4.teachername.choices += [(r.id, r.name) for r in teacher]
    # 进入模板，传递参数
    return render_template('eduadmin.html',
                           myself=myself,
                           Dep=Department, Cla=Class, Type=Coursetype, Tea=Teacher, Cour=Course,
                           form1=form1, form2=form2, form3=form3, form4=form4,
                           student=student, teacher=teacher, course=course, courseplan=courseplan,
                           department=department, classs=classs, coursetype=coursetype)
