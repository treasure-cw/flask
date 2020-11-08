# 从flask包中导入蓝图
from flask import Blueprint
# 声明蓝图对象student
student = Blueprint('student', __name__)

from .views import *
from .forms import *
