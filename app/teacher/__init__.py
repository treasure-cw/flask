# 从flask包中导入蓝图
from flask import Blueprint
# 声明蓝图对象teacher
teacher = Blueprint('teacher', __name__)

from .views import *
from .forms import *
