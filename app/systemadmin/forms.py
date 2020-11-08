from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, Regexp

'''
添加教务员表单：
name:教务员姓名（输入），输入验证
password:密码（输入），输入验证，正则表达式验证（长度1-20，字母数字）
submit1:添加（点击）
'''


class AddEduadminForm(FlaskForm):
    name = StringField(label='昵称', validators=[DataRequired(u'必须输入数据')])
    password = PasswordField(label='密码', validators=[DataRequired(u'必须输入数据'),
                                                     Regexp("^\\w{1,20}$", message="密码长度1-20位，仅可输入字母或数字")])
    submit1 = SubmitField(label='添加')


'''
添加系所表单：
name:系所名称（输入），输入验证
submit2:添加（点击）
'''


class AddDepartmentForm(FlaskForm):
    name = StringField(label='系所名称', validators=[DataRequired(u'必须输入数据')])
    submit2 = SubmitField(label='添加')


'''
添加专业表单：
departmentname:所属系id（选择）（对用户可见为系名称），输入验证
name:专业名称（输入），输入验证
submit3:添加（点击）
'''


class AddMajorForm(FlaskForm):
    departmentname = SelectField(label='系所名称', validators=[DataRequired(u'必须输入数据')], choices=[])
    name = StringField(label='专业名称', validators=[DataRequired(u'必须输入数据')])
    submit3 = SubmitField(label='添加')


'''
添加班级表单：
majorname:专业id（选择）（对用户可见为系名称），输入验证
name:班级名称（输入），输入验证
startyear:入学时间（输入），输入验证
submit5:添加（点击）
'''


class AddClassForm(FlaskForm):
    majorname = SelectField(label='专业名称', validators=[DataRequired(u'必须输入数据')], choices=[])
    name = StringField(label='班级名称', validators=[DataRequired(u'必须输入数据')])
    startyear = DateField(label='入学时间', validators=[DataRequired(u'必须输入数据')])
    submit5 = SubmitField(label='添加')


'''
添加课程类别表单：
name:课程类别名称（输入），输入验证
submit4:添加（点击）
'''


class AddCoursetypeForm(FlaskForm):
    name = StringField(label='类别名称', validators=[DataRequired(u'必须输入数据')])
    submit4 = SubmitField(label='添加')


'''
重置密码表单：
password:密码（输入），输入验证，正则表达式验证（长度1-20，字母数字）
passwordrest:重复密码（输入），输入验证，相等验证
submit5:添加（点击）
'''


class ChangePassword(FlaskForm):
    password = PasswordField(label='密码', validators=[DataRequired(u'必须输入数据'),
                                                     Regexp("^\\w{1,20}$", message="密码长度1-20位，仅可输入字母或数字")])
    passwordrest = PasswordField(label='重复密码', validators=[DataRequired(u'必须输入数据'), EqualTo('password', u'两次输入不一致')])
    submit5 = SubmitField(label='确认修改')
