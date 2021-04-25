# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/25 10:40
import os

from flask import render_template, Blueprint

from app.specs import spec

_here = os.path.dirname(__file__)
template_folder = os.path.join(_here, 'templates')
static_folder = os.path.join(template_folder, 'static')

openapi_bl = Blueprint("openapi", __name__)


@openapi_bl.route('/swag')
def swag():
    """swag文档"""
    return render_template("swag.html", spec_url=spec.config.spec_url)


@openapi_bl.route('/redoc')
def redoc():
    """redoc文档"""
    return render_template("redoc.html", spec_url=spec.config.spec_url)


@openapi_bl.route('/')
def index():
    return render_template("index.html", spec_url=spec.config.spec_url)
