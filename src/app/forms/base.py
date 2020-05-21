# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 17:21
import traceback

from flask import request
from wtforms import Form

from app.utils.exceptions import ParameterException


class BaseForm(Form):
    """表单、参数验证基类"""

    def __init__(self, **kwargs):
        content_type = request.content_type
        if content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
        elif 'multipart/form-data' in str(content_type):
            data = request.form.to_dict()
        elif content_type == 'application/json':
            data = request.json
        else:
            data = {}
        args = request.args.to_dict()
        if kwargs:
            data.update(**kwargs)
        print(data)
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
