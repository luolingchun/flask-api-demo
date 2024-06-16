# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2024/6/11 9:46
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import String, Column

from app.form.poi import CreatePOIBody
from app.model import Base, db


class POI(Base):
    __tablename__ = f"poi"
    __table_args__ = ({"comment": "地名表"})
    name = Column(String(32), nullable=False, unique=True, comment="名称")
    location = Column(Geometry(geometry_type="POINT", srid=4326), comment="位置")

    @staticmethod
    def create(body: CreatePOIBody):
        poi = POI()

        poi.name = body.name
        poi.location = f"SRID=4326;POINT({body.lng} {body.lat})"

        db.session.add(poi)
        db.session.commit()

    def data(self):
        if self.location:
            point = to_shape(self.location)
            location = [point.x, point.y]
        else:
            location = None
        return {
            "id": self.id,
            "name": self.name,
            "location": location
        }
