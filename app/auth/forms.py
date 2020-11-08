from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, Length


'''
登录表单：
userid:账户 输入验证，正则表达式验证（长度验证，首位验证）
password:密码
submit:提交按钮
'''


class LoginForm(FlaskForm):
    userid = StringField(label='账号',
                         validators=[DataRequired(u'必须输入数据'),
                                     Regexp("^[1-9][0-9]{7,11}$",message="账号格式有误")])
    password = PasswordField(label='密码',
                             validators=[DataRequired(u'必须输入数据')])
    submit = SubmitField(label='提交')
