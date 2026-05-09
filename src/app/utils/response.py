def response(code=0, message="ok", **kwargs):
    """响应体数据格式"""
    data = {"code": code, "message": message}
    data.update(**kwargs)
    return data
