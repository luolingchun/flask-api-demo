# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53

from . import create_app

app = create_app()


@app.route('/')
def index():
    return "欢迎使用"


if __name__ == '__main__':
    app.run(debug=True)
