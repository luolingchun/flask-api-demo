# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, length, EqualTo, Regexp, Optional

from .base import BaseForm


class RegisterForm(BaseForm):
    name = StringField(
        validators=[DataRequired(),
                    length(min=4, max=32)
                    ]
    )
    password = PasswordField(
        validators=[DataRequired(),
                    EqualTo('confirm_password'),
                    length(min=6)
                    ]
    )
    confirm_password = PasswordField(
        validators=[DataRequired()]
    )
    email = StringField(
        validators=[
            Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'),
            Optional()
        ]
    )


class LoginForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


class ModifyPasswordForm(BaseForm):
    old_password = PasswordField(validators=[DataRequired(), length(min=6)])
    new_password = PasswordField(validators=[DataRequired(), length(min=6)])
