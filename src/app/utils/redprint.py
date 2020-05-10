# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:16
from flask import Blueprint


class Redprint:
    """红图，提供route装饰器、注册蓝图功能"""

    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp: Blueprint, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
