# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/18 9:34
from typing import List, Any, Dict

from pydantic import BaseModel, Field
from rq.job import JobStatus

from app.form import PageModel


class JobQuery(PageModel):
    status: JobStatus = Field(..., description="job status")


class JobPath(BaseModel):
    job_id: str = Field(..., description="job ID")


class JobResponse(BaseModel):
    job_id: str = Field(..., description="UUID")
    args: List[Any] = Field(None, description="parameter")
    kwargs: Dict[str, Any] = Field(None, description="keyword parameters")
    result: Any = Field(None, description="result")
    enqueued_at: str = Field(None, description="time queued")
    started_at: str = Field(None, description="time started")
    ended_at: str = Field(None, description="time ended")
    exc_info: str = Field(None, description="exception info")
    origin: str = Field(None, description="origin")
    job_status: str = Field(None, description="job status")
    ttl: str = Field(None, description="ttl")
