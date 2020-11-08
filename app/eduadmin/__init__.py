# 从flask包中导入蓝图
from flask import Blueprint

# 声明蓝图对象eduadmin
eduadmin = Blueprint('eduadmin', __name__)

from .views import *
from .forms import *
