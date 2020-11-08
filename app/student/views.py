from flask import render_template, redirect, url_for, request, flash
from . import student
from .forms import *
from ..models import *
from .. import db
from flask_login import login_user, logout_user, login_required, current_user


current_file = 'student\\views.py'


'''
选课业务：
接收form表单的POST请求；
对form表单提交的选课列表进行批操作；
'''


@student.route('/addcourse/<string:id>', methods=['POST'])
def addcourse(id):
    # lis:表单提交的选择的课程排课号
    lis = request.form.getlist('chk')
    for l in lis:
        list_course = Courseplan.query.filter_by(id=l).all()
        course_name = Course.query.filter_by(id=list_course[0].courseid).first().name
        if list_course[0].num > 0:
            me = Choice(studentid=id, courseplanid=l, score=0)
            db.session.add(me)
            db.session.commit()
            for lc in list_course:
                lc.num = lc.num - 1
                db.session.commit()
        else:
            flash(f'{course_name}课程已经满员', 'warning')
    return redirect(url_for('student.stu', id=id))


'''
退课业务：
接收form表单的POST请求；
对form表单提交的退课列表进行批操作；
'''


@student.route('/deletecourse/<string:id>', methods=['POST'])
def deletecourse(id):
    # lis:表单提交的退选的课程排课号
    lis = request.form.getlist('chk')
    for l in lis:
        me = Choice.query.filter_by(studentid=id, courseplanid=l).first()
        db.session.delete(me)
        db.session.commit()
        list_course = Courseplan.query.filter_by(id=l).all()
        for lc in list_course:
            lc.num = lc.num + 1
            db.session.commit()
    return redirect(url_for('student.stu', id=id))


'''
学生主界面：
先行登录验证通过才能访问；
参数id为学生账号；
'''


@student.route('/stu/<string:id>', methods=['GET', 'POST'])
@login_required
def stu(id):
    # myself:当前用户对象
    myself = Student.query.filter_by(id=id).first()
    # courseplan:当前用户所在班级开设课程
    courseplan = Courseplan.query.filter_by(classid=myself.classid).all()
    # choice:当前用户所选课（already）
    choice = Choice.query.filter_by(studentid=id).all()
    # courseids[]:当前用户已选课程的课程号（顺序）
    # coursescores[]:当前用户已选课程的学分（顺序）
    # coursetypes[]:当前用户已选课程的课程类型（顺序）
    # seqtime[]:当前用户已选课程的上课时间（顺序）
    # table_class[]:当前用户课程表
    # sumscores:总成绩（课程[x]成绩*课程[x]学分数;x为变量）
    # sumstudyscores:总学分数
    courseids = []
    coursescores = []
    coursetypes = []
    seqtime = []
    table_class = [['', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', '']]
    sumscores = 0
    sumstudyscores = 0
    for ch in choice:
        # cp:choice中的一个排课对象（顺序）
        cp = Courseplan.query.filter_by(id=ch.courseplanid).first()
        courseids.append(cp.courseid)
        # C:choice中的一个课程对象（顺序）
        C = Course.query.filter_by(id=courseids[-1]).first()
        coursescores.append(C.studyscore)
        sumscores += (float(ch.score) * float(C.studyscore))
        sumstudyscores += float(C.studyscore)
        if C.tag == 0:
            coursetypes.append("必修课")
        elif C.tag == 1:
            coursetypes.append("专业限选课")
        else:
            coursetypes.append("通选限选课")
        # 上课时间在数据库中的存放形式是:[day:location,......]tag
        # tag:周次表示，'0'表示全周；'1'表示单周；'2'表示双周
        # day:表示周内某天，'1'--'7'分别表示周一至周日
        # location:表示课程节次，'1'--'5'分表表示第一大节至第五大节课
        txt = ""
        nums = cp.seq[-1]
        seq = cp.seq[1:-2].split(',')
        # 把课程放入课表
        for s in seq:
            txt += f"周{s[0]} 第{s[-1]}大节,"
            table_class[int(s[-1]) - 1][int(s[0]) - 1] = C.name
        # 把描述放入seqtime[]
        if nums == '0':
            txt += "全周"
        elif nums == '1':
            txt += "单周"
        elif nums == '2':
            txt += "双周"
        seqtime.append(txt)
    # mychoice:当前用户所选课的排课编号
    mychoice = []
    for c in choice:
        mychoice.append(c.courseplanid)
    # course0[]:当前用户所在班级开设的必修课（可选的）
    # course0seq[]:当前用户所在班级开设的必修课的上课时间（可选的）
    # course1[]:当前用户所在班级开设的专业限选课（可选的）
    # course1seq[]:当前用户所在班级开设的专业限选课的上课时间（可选的）
    # course2[]:当前用户所在班级开设的通选限选课（可选的）
    # course2seq[]:当前用户所在班级开设的通选限选课的上课时间（可选的）
    course0 = []
    course0seq = []
    course1 = []
    course1seq = []
    course2 = []
    course2seq = []
    for cp in courseplan:
        # 如果课程还没选满
        if cp.num > 0:
            # current_course:当前课程
            # temp_tag:标识，标识当前课程是否与选课冲突，初始值为0
            temp_tag = 0
            current_course = Course.query.filter_by(id=cp.courseid).first()
            if current_course.tag == '0':
                # seq:上课时间信息分割
                seq = cp.seq[1:-2].split(',')
                # 如果当前课程与课表信息冲突，标识置为1
                for s in seq:
                    if table_class[int(s[-1]) - 1][int(s[0]) - 1] != "":
                        temp_tag = 1
                        break
                # 没有冲突，加入当前课程排课对象；加入当前课程上课时间
                if temp_tag == 0:
                    course0.append(cp)
                    txt = ""
                    nums = course0[-1].seq[-1]
                    for s in seq:
                        txt += f"周{s[0]} 第{s[-1]}大节,"
                    if nums == '0':
                        txt += "全周"
                    elif nums == '1':
                        txt += "单周"
                    elif nums == '2':
                        txt += "双周"
                    course0seq.append(txt)
            elif current_course.tag == '1':
                seq = cp.seq[1:-2].split(',')
                for s in seq:
                    if table_class[int(s[-1]) - 1][int(s[0]) - 1] != "":
                        temp_tag = 1
                        break
                if temp_tag == 0:
                    course1.append(cp)
                    txt = ""
                    nums = course1[-1].seq[-1]
                    for s in seq:
                        txt += f"周{s[0]} 第{s[-1]}大节,"
                    if nums == '0':
                        txt += "全周"
                    elif nums == '1':
                        txt += "单周"
                    elif nums == '2':
                        txt += "双周"
                    course1seq.append(txt)
            else:
                seq = cp.seq[1:-2].split(',')
                for s in seq:
                    if table_class[int(s[-1]) - 1][int(s[0]) - 1] != "":
                        temp_tag = 1
                        break
                if temp_tag == 0:
                    course2.append(cp)
                    txt = ""
                    nums = course2[-1].seq[-1]
                    for s in seq:
                        txt += f"周{s[0]} 第{s[-1]}大节,"
                    if nums == '0':
                        txt += "全周"
                    elif nums == '1':
                        txt += "单周"
                    elif nums == '2':
                        txt += "双周"
                    course2seq.append(txt)
    # classroom: 上课节次名称
    classname = ['1-2节', '3-4节', '5-6节', '7-8节', '9-10节']
    # 计算平均学分绩点
    # xf:平均学分绩点
    if sumstudyscores == 0:
        xf = 0
    else:
        xf = sumscores / sumstudyscores
    # 进入模板，传递参数
    return render_template('student.html',
                           Cla=Class, Cou=Course, Tea=Teacher, table_class=table_class,
                           classname=classname,
                           myself=myself, mychoice=mychoice, course0=course0, course1=course1, course2=course2,
                           course0seq=course0seq, course1seq=course1seq, course2seq=course2seq, xf=xf,
                           choice=choice, courseids=courseids, coursetypes=coursetypes, seqtime=seqtime,
                           coursescores=coursescores)
