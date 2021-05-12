# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:36

from wtforms import StringField, IntegerField, FieldList, PasswordField
from wtforms.validators import DataRequired, Optional, length, Regexp, EqualTo

from . import BaseForm


class AddUserForm(BaseForm):
    name = StringField(validators=[DataRequired(), length(min=4, max=32)])
    password = PasswordField(validators=[DataRequired(), EqualTo('confirm_password'), length(min=6)])
    confirm_password = PasswordField(validators=[DataRequired()])
    email = StringField(
        validators=[
            Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'),
            Optional()
        ])
    role_ids = FieldList(IntegerField(validators=[DataRequired()]), default=[1])
    key_list = ['role_ids']


class CreateRoleForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    describe = StringField(validators=[Optional()])
    auth_ids = FieldList(StringField(validators=[DataRequired()]))
    key_list = ['auth_ids']


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
    key_list = ['role_ids']


class RoleAuthForm(BaseForm):
    role_id = IntegerField(validators=[DataRequired()])
    # auth_ids只能接收object，不能接收字符串
    auth_ids = FieldList(IntegerField(validators=[DataRequired()]), validators=[DataRequired()], _prefix=',')
    key_list = ['auth_ids']


class ModifyPasswordForm(BaseForm):
    password = PasswordField(validators=[DataRequired(), length(min=6)])
