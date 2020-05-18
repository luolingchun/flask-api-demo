# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:36
from wtforms import StringField, IntegerField, FieldList
from wtforms.validators import DataRequired, Optional

from .base import BaseForm


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
    role_ids = FieldList(IntegerField(validators=[DataRequired()]), validators=[DataRequired()])


class RoleAuthForm(BaseForm):
    role_id = IntegerField(validators=[DataRequired()])
    auth_ids = FieldList(IntegerField(validators=[DataRequired()]), validators=[DataRequired()])
