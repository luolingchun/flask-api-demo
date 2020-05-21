# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:36
from flask import request
from wtforms import StringField, IntegerField, FieldList
from wtforms.validators import DataRequired, Optional

from .base import BaseForm
from ..utils.exceptions import ParameterException


class CreateRoleForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    describe = StringField(validators=[Optional()])
    # auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


class GetRolesForm(BaseForm):
    page = IntegerField(validators=[Optional()], default=0)
    page_size = IntegerField(validators=[Optional()], default=20)


class UpdateRoleForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    describe = StringField(validators=[Optional()])


class GetUsersForm(BaseForm):
    page = IntegerField(validators=[Optional()], default=0)
    page_size = IntegerField(validators=[Optional()], default=20)
    # role_id = IntegerField(validators=[Optional()], )


class UserRoleForm(BaseForm):
    user_id = IntegerField(validators=[DataRequired()])
    role_ids = FieldList(IntegerField(validators=[DataRequired()]), validators=[DataRequired()], _prefix=',')


class RoleAuthForm(BaseForm):
    role_id = IntegerField(validators=[DataRequired()])
    # auth_ids只能接收object，不能接收字符串
    auth_ids = FieldList(IntegerField(validators=[DataRequired()]), validators=[DataRequired()], _prefix=',')

    def __init__(self):
        # content-type为multipart/form-data或application/x-www-form-urlencoded时:
        # 将auth_ids转化为object
        auth_ids = request.form.get('auth_ids')
        try:
            assert auth_ids.startswith('[')
            assert auth_ids.endswith(']')
            kwargs = {'auth_ids': list(eval(auth_ids))} if auth_ids else {}
        except:
            raise ParameterException(message='参数错误：auth_ids')
        super(RoleAuthForm, self).__init__(**kwargs)
