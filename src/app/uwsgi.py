# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53

from flask import redirect, url_for

from app import create_app

app = create_app()


@app.route('/')
def index():
    """根目录重定向到apidocs"""
    # print(app.url_map)
    return redirect(url_for('flasgger.apidocs'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
