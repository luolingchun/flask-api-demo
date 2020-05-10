# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11

from wtforms import  StringField
from wtforms.validators import DataRequired, length

from .base import BaseForm


class UserForm(BaseForm):
    username = StringField(label='username', validators=[DataRequired(), length(min=5, max=32)])
    password = StringField(label='password', validators=[DataRequired(), length(min=6)])
