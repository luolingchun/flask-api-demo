# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 17:21
import traceback

from flask import request
from wtforms import Form

from app.utils.exceptions import ContentTypeException, ParameterException


class BaseForm(Form):
    def __init__(self):
        content_type = request.content_type
        if content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
        elif content_type and 'multipart/form-data' in content_type:
            data = request.form.to_dict()
        elif content_type == 'application/json':
            data = request.json
        else:
            data = {}
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        try:
            valid = super(BaseForm, self).validate()
        except Exception as e:
            traceback.print_exc(e)
            raise ParameterException(message='参数验证错误')
        if not valid:
            raise ParameterException(message=self.errors)

        return self
