from pydantic import BaseModel, Field


class CreatePOIBody(BaseModel):
    name: str = Field(..., description="名称")
    lng: float = Field(..., description="经度")
    lat: float = Field(..., description="纬度")
