from sqlalchemy import ForeignKey
from . import db, login_manager
from flask_login import UserMixin

'''
系统管理员：
id 系统管理员账号
name 系统管理员姓名
password 系统管理员密码            
'''


class Sysadmin(UserMixin, db.Model):
    __tablename__ = 'sysadmin'
    id = db.Column(db.CHAR(8), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(20), nullable=False)


'''
教务员：
id 教务员账号
name 教务员姓名
password 教务员密码
'''


class Eduadmin(UserMixin, db.Model):
    __tablename__ = 'eduadmin'
    id = db.Column(db.CHAR(9), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(20), nullable=False)


'''
教师：
id 教师账号
name 教师姓名
departmentid 教师所属系编号
password 教师密码
'''


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.CHAR(10), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    departmentid = db.Column(db.CHAR(7), ForeignKey('department.id'))
    password = db.Column(db.VARCHAR(20), nullable=False)


'''
学生：
id 学生账号
name 学生姓名
sex 学生行别
birthday 学生出生日期
classid 学生所属班级编号
'''


class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.CHAR(12), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    sex = db.Column(db.CHAR(2), nullable=False)
    brithday = db.Column(db.DATE, nullable=False)
    classid = db.Column(db.CHAR(8), ForeignKey('class.id'))
    password = db.Column(db.VARCHAR(20), nullable=False)


'''
载入当前用户
判断id长度以确定用户类型
'''


@login_manager.user_loader
def load_user(user_id):
    if len(user_id) == 8:
        return Sysadmin.query.get(user_id)
    if len(user_id) == 9:
        return Eduadmin.query.get(user_id)
    if len(user_id) == 10:
        return Teacher.query.get(user_id)
    if len(user_id) == 12:
        return Student.query.get(user_id)


'''
学院：
id 学院编号
name 学院名称
'''


class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.CHAR(5), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)


'''
系：
id 系编号
collegeid 系所属学院编号
name 系名称
'''


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.CHAR(6), primary_key=True)
    collegeid = db.Column(db.CHAR(5), ForeignKey('college.id'))
    name = db.Column(db.VARCHAR(20), nullable=False)


'''
专业：
id 专业编号
departmentid 专业所属系编号
name 专业名称
'''


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.CHAR(7), primary_key=True)
    departmentid = db.Column(db.CHAR(6), ForeignKey('department.id'))
    name = db.Column(db.VARCHAR(20), nullable=False)


'''
班级：
id 班级编号
majorid 班级所属专业编号
name 班级名称
startyear 入学年份
'''


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.CHAR(8), primary_key=True)
    majorid = db.Column(db.CHAR(7), ForeignKey('major.id'))
    name = db.Column(db.VARCHAR(20), nullable=False)
    startyear = db.Column(db.DATE, nullable=False)


'''
课程类别：
id 类别编号（0：必修课1：专业限选课2：通识限选课）
name 类别名称
'''


class Coursetype(db.Model):
    __tablename__ = 'coursetype'
    id = db.Column(db.CHAR(1), primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False)


'''
课程：
id 课程编号
tag 课程所属类别
name 课程名称
studyhour 课程学时
studyscore 课程学分
'''


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.CHAR(8), primary_key=True)
    tag = db.Column(db.CHAR(1), ForeignKey('coursetype.id'))
    name = db.Column(db.VARCHAR(20), nullable=False)
    studyhour = db.Column(db.INTEGER, nullable=False)
    studyscore = db.Column(db.FLOAT, nullable=False)


'''
排课计划：
id 排课编号
classid 允许选课班级编号
courseid 排课课程编号
seq 课程序列
teacherid 上课教师编号
num 课程限制人数
semester 开课学期
'''


class Courseplan(db.Model):
    __tablename__ = 'courseplan'
    id = db.Column(db.CHAR(12), primary_key=True)
    classid = db.Column(db.CHAR(8), ForeignKey('class.id'), primary_key=True)
    courseid = db.Column(db.CHAR(8), ForeignKey('course.id'))
    seq = db.Column(db.VARCHAR(40), nullable=False)
    teacherid = db.Column(db.CHAR(10), ForeignKey('teacher.id'))
    num = db.Column(db.INTEGER, nullable=False)
    semester = db.Column(db.VARCHAR(20), nullable=False)


'''
选课计划：
studentid 选课学生编号
courseplanid 排课编号
score 成绩
'''


class Choice(db.Model):
    __tablename__ = 'choice'
    studentid = db.Column(db.CHAR(12), ForeignKey('student.id'), primary_key=True)
    courseplanid = db.Column(db.CHAR(12), ForeignKey('courseplan.id'), primary_key=True)
    score = db.Column(db.FLOAT, nullable=True)
