from flask import render_template, redirect, url_for, request
from . import teacher
from .forms import *
from ..models import *
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from werkzeug.utils import secure_filename
'''
添加分数业务：
myid:当前登录用户id；
获取要给分数的choice对象；
按照表单内容进行给分；
重定向到教师主页面；
批操作；
'''


@teacher.route('/addscore/<string:myid>', methods=['POST'])
def addscore(myid):
    # 分数，学生id，排课id列表
    list_score = request.form.getlist('score')
    list_sid = request.form.getlist('sid')
    list_cid = request.form.getlist('cid')
    # 批处理，按照顺序给分
    for index in range(len(list_score)):
        me = Choice.query.filter_by(studentid=list_sid[index], courseplanid=list_cid[index]).first()
        me.score = list_score[index]
        db.session.commit()
    # 重定向到教师主页面
    return redirect(url_for('teacher.tea', id=myid))


'''
教师主界面：
先行登录验证通过才能访问；
参数id为教师账号；
'''


@teacher.route('/tea/<string:id>', methods=['GET', 'POST'])
@login_required
def tea(id):
    # myself:当前登录用户对象
    myself = Teacher.query.filter_by(id=id).first()
    # courseplan[]:当前教师所上的全部课程对象列表（排课）
    # choice[]:当前所有选课对象列表
    # courseids[]:当前教师所教授全部课程的课程id列表（去重）
    # lis[]:当前教师所教授全部课程的课程id列表（未去重）
    # courseseq[]:当前教师所教授全部课程的上课时间列表（去重）
    # openclass[]:当前教师所教授全部课程的开课班级列表（去重）
    # sum[]:当前教师所教授全部课程的选课人数列表（去重）
    courseplan = Courseplan.query.filter_by(teacherid=id).all()
    choice = Choice.query.all()
    courseids = []
    lis = []
    courseseq = []
    openclass = []
    sum = []
    for coup in courseplan:
        # 将排课对象的课程id加入lis
        lis.append(coup.id)
        # 如果当前排课对象的课程id没有在courseids[]中出现则进行下属操作
        # 去重
        if coup.courseid not in courseids:
            # ssum:当前选coup.courseid的人数
            ssum = Choice.query.filter_by(courseplanid=coup.id).count()
            # 将ssum加入到sum[]
            # 将课程id加入courseids[]
            sum.append(ssum)
            courseids.append(coup.courseid)
            # 将上课时间可视化
            # 上课时间在数据库中的存放形式是:[day:location,......]tag
            # tag:周次表示，'0'表示全周；'1'表示单周；'2'表示双周
            # day:表示周内某天，'1'--'7'分别表示周一至周日
            # location:表示课程节次，'1'--'5'分表表示第一大节至第五大节课
            txt = ""
            nums = coup.seq[-1]
            seq = coup.seq[1:-2].split(',')
            # 将上课时间拼接
            for s in seq:
                txt += f"周{s[0]} 第{s[-1]}大节,"
            if nums == '0':
                txt += "全周"
            elif nums == '1':
                txt += "单周"
            elif nums == '2':
                txt += "双周"
            # 添加到courseseq中
            courseseq.append(txt)
            # classname:开课班级名称
            classname = Class.query.filter_by(id=coup.classid).first().name
            # 将开课班级加入openclass[]
            openclass.append(f",{classname}")
        # 如果重复
        # 说明一个课程多个班级选课
        else:
            # 找到当前下标
            # ind:下标
            ind = courseids.index(coup.courseid)
            # 将新的班级吗追加到openclass中
            classname = Class.query.filter_by(id=coup.classid).first().name
            openclass[ind] += f",{classname}"
    # mychoice[]:当前教师所教授的课&&被学生选择
    # mychoice1[]:当前教师所教授的课&&被学生选择&&没给分
    # mychoice2[]:当前教师所教授的课&&被学生选择&&已经给分
    mychoice = []
    mychoice1 = []
    mychoice2 = []
    # 将数据添加到上述列表
    for c in choice:
        if c.courseplanid in lis:
            mychoice.append(c)
        if c.courseplanid in lis and float(c.score) == 0.0:
            mychoice1.append(c)
        if c.courseplanid in lis and float(c.score) != 0.0:
            mychoice2.append(c)
    # courseids1[]:mychoice[]里面的课程编号列表
    # courseids11[]:mychoice1[]里面的课程编号列表
    # courseids111[]:mychoice2[]里面的课程编号列表
    courseids1 = []
    courseids11 = []
    courseids111 = []
    # 将课程编号加入到上述列表
    for c in mychoice:
        courseids1.append(Courseplan.query.filter_by(id=c.courseplanid).first().courseid)
    for c in mychoice1:
        courseids11.append(Courseplan.query.filter_by(id=c.courseplanid).first().courseid)
    for c in mychoice2:
        courseids111.append(Courseplan.query.filter_by(id=c.courseplanid).first().courseid)
    # 进入模板，传递参数
    return render_template('teacher.html',
                           Cou=Course, Stu=Student, Cla=Class, myself=myself,
                           courseplan=courseplan, mychoice=mychoice, mychoice1=mychoice1, mychoice2=mychoice2,
                           courseids=courseids, courseseq=courseseq,
                           courseids1=courseids1, courseids11=courseids11, courseids111=courseids111,
                           openclass=openclass, sum=sum)


'''
Excel录入文件业务：
myid:当前登录用户的id；
接收表单的post数据；
将Excel文件存入项目文件夹；
将Excel文件中的成绩按照顺序写入数据库中；
重定向到教师主页面
批操作；
'''


@teacher.route('/upload/<string:myid>', methods=['POST'])
def upload(myid):
    if request.method == 'POST':
        # f:表单提交的文件
        # basepath:当前项目的目录
        # upload_path:文件保存位置
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, '../static/uploads/')
        # 保存Excel文件
        f.save(upload_path + secure_filename(f.filename))
        # 从xlrd包中导入open_workbook
        from xlrd import open_workbook
        # bk:open_workbook对象，文件位置为upload_path，使用utf-8编码
        bk = open_workbook(upload_path + secure_filename(f.filename), encoding_override="utf-8")
        # 捕捉Excel文件不存在的错误
        try:
            sh = bk.sheets()[0]
        except Exception:
            print("no sheet in %s named sheet1" % f.filename)
        else:
            # 将Excel文件中内容导入数据库choice表中
            # nrows:Execl文件行数
            nrows = sh.nrows
            for i in range(1, nrows):
                row_date = sh.row_values(i)
                n = i - 1
                me = Choice.query.filter_by(courseplanid=str(int(row_date[0])),
                                            studentid=str(int(row_date[1]))).first()
                me.score = row_date[2]
                db.session.commit()
        # 重定向到教师主页面
        return redirect(url_for('teacher.tea', id=myid))
    return true
