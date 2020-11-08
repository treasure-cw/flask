from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Regexp, Length

'''
添加学生表单：
name:学生姓名（输入），输入验证
classname:班级id（选择）（对用户可见为班级姓名），输入验证
sex:性别（选择），输入验证
birthday:生日（输入），输入验证
password:密码（输入），输入验证，正则表达式验证（长度1-20，字母数字）
submit1:添加（点击）
'''


class AddStudentForm(FlaskForm):
    name = StringField(label='姓名', validators=[DataRequired(u'必须输入数据')])
    classname = SelectField(label='班级', validators=[DataRequired(u'必须输入数据')], choices=[])
    sex = SelectField(label='性别', validators=[DataRequired(u'必须输入数据')], choices=['女', '男'])
    birthday = DateField(label='出生日期', validators=[DataRequired(u'必须输入数据')])
    password = PasswordField(label='密码', validators=[DataRequired(u'必须输入数据'),
                                                     Regexp("^\\w{1,20}$", message="密码长度1-20位，仅可输入字母或数字")])
    submit1 = SubmitField(label='添加')


'''
添加教师表单：
departmentname:所属系id（选择）（对用户可见为系名称），输入验证
name:教师姓名（输入），输入验证
password:密码（输入），输入验证，正则表达式验证（长度1-20位，字母数字）
submit2:添加（点击）
'''


class AddTeacherForm(FlaskForm):
    departmentname = SelectField(label='系所', validators=[DataRequired(u'必须输入数据')], choices=[])
    name = StringField(label='姓名', validators=[DataRequired(u'必须输入数据')])
    password = PasswordField(label='密码', validators=[DataRequired(u'必须输入数据'),
                                                     Regexp("^\\w{1,20}$", message="密码长度1-20位，仅可输入字母或数字")])
    submit2 = SubmitField(label='添加')


'''
添加课程表单：
typename:课程类别id（选择）（用户可见为类别名称），输入验证
name:课程名称（输入），输入验证
studyhour:学时（选择），输入验证
studyscore:学分（选择），输入验证
submit3:添加（点击）
'''


class AddCourseForm(FlaskForm):
    typename = SelectField(label='课程类别', validators=[DataRequired(u'必须输入数据')], choices=[])
    name = StringField(label='课程名称', validators=[DataRequired(u'必须输入数据')])
    studyhour = SelectField(label='课程学时', validators=[DataRequired(u'必须输入数据')],
                            choices=[16, 32, 48, 64])
    studyscore = SelectField(label='课程学分', validators=[DataRequired(u'必须输入数据')],
                             choices=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6])
    submit3 = SubmitField(label='添加')


'''
添加排课信息表单
coursename:课程id（选择）（用户可见为课程名称），输入验证
teachername:教师id（选择）（用户可见为教师姓名），输入验证
classname:可选班级id（选择）（用户可见为班级名称），输入验证
seq:上课时间（输入），输入验证，正则表达式验证（待修改）
num:选课人数上限（输入），输入验证
semester:开课学期（选择），输入验证
submit4:添加（点击）
'''


class AddCourseplanForm(FlaskForm):
    coursename = SelectField(label='课程', validators=[DataRequired(u'必须输入数据')], choices=[])
    teachername = SelectField(label='任课教师', validators=[DataRequired(u'必须输入数据')], choices=[])
    classname = SelectField(label='可选班级', validators=[DataRequired(u'必须输入数据')], choices=[])
    seq = StringField(label='上课时间', validators=[DataRequired(u'必须输入数据')])
    num = IntegerField(label='人数上限', validators=[DataRequired(u'必须输入数据')])
    semester = SelectField(label='开设学期', validators=[DataRequired(u'必须输入数据')],
                           choices=["2020-2021春季学期", "2020-2021秋季学期", "2021-2022春季学期", "2021-2022秋季学期"])
    submit4 = SubmitField(label='添加')
