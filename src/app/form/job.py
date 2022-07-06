# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/18 9:34
from typing import List, Any, Dict

from pydantic import BaseModel, Field
from rq.job import JobStatus

from app.form import PageModel


class JobQuery(PageModel):
    status: JobStatus = Field(..., description="任务状态")


class JobPath(BaseModel):
    job_id: str = Field(..., description="任务UUID")


class JobResponse(BaseModel):
    job_id: str = Field(..., description="UUID")
    args: List[Any] = Field(None, description="参数")
    kwargs: Dict[str, Any] = Field(None, description="关键字参数")
    result: Any = Field(None, description="结果")
    enqueued_at: str = Field(None, description="入队时间")
    started_at: str = Field(None, description="开始时间")
    ended_at: str = Field(None, description="结束时间")
    exc_info: str = Field(None, description="异常信息")
    origin: str = Field(None, description="所在队列")
    job_status: str = Field(None, description="状态")
    ttl: str = Field(None, description="存活时间")
