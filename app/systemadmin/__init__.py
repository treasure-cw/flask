from flask import Blueprint

systemadmin = Blueprint('systemadmin', __name__)

from .views import *
from .forms import *
