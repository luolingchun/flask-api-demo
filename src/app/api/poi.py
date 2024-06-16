# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2024/6/11 9:48
from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from sqlalchemy import select

from app.config import API_PREFIX, JWT
from app.form import PageModel
from app.form.poi import CreatePOIBody
from app.model import db, get_offset_limit, get_total_page
from app.model.poi import POI
from app.utils.exceptions import ResourceExistException
from app.utils.response import response

__version__ = "/v1"
__bp__ = "/poi"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="地名", description="地名管理")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag], abp_security=JWT)


@api.post("", summary="创建地名")
def create_book(body: CreatePOIBody):
    poi = db.session.execute(select(POI).where(POI.name == body.name)).scalar()  # type: ignore
    if poi:
        raise ResourceExistException()
    POI.create(body)
    return response()


@api.get("", summary="获取地名数据列表")
def get_poi(query: PageModel):
    offset, limit = get_offset_limit(query.page, query.page_size)
    poi_list = db.session.execute(select(POI).order_by(POI.id.desc()).offset(offset).limit(limit)).scalars()
    total, total_page = get_total_page(POI.id, [], limit)
    data = [poi.data() for poi in poi_list]
    return response(data=data, total=total, total_page=total_page)
