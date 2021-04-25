# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
