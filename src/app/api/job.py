# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/10/10 10:28
import math
from datetime import timedelta
from uuid import uuid1

from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag
from rq.command import send_stop_job_command
from rq.exceptions import InvalidJobOperation
from rq.job import Job

from app.config import API_PREFIX, JWT
from app.form.job import QueryJob, PathJob, QueryJobResponse
from app.jobs import job_test
from app.rq import rq2
from app.rq.queue import default_queue
from app.utils.enums import PermissionGroup
from app.utils.exceptions import JobNotExistException, JobNotRetryException
from app.utils.jwt_tools import role_required, permission
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/job'
tag = Tag(name=__version__ + __bp__, description="用户")
api = APIBlueprint(__bp__, __name__, url_prefix=API_PREFIX + __version__ + __bp__, abp_tags=[tag], abp_security=JWT)


@api.post('')
@permission(name='添加异步任务', module=PermissionGroup.JOB, uuid='26017994-9c06-11eb-84be-8cec4baea5d8')
# @role_required
def add_job():
    """添加异步任务"""
    job_id = str(uuid1())
    default_queue.enqueue(job_test, args=(1, 4, job_id), job_id=job_id, job_timeout=3600)
    return response(data=job_id)


@api.get('', responses={"200": QueryJobResponse})
@permission(name='查询异步任务', module=PermissionGroup.JOB, uuid='46ffb3d9-9c06-11eb-981b-8cec4baea5d8')
# @role_required
def query_job(query: QueryJob):
    """查询异步任务"""
    page = query.page
    page_size = query.page_size
    status = query.status

    if status == "queued":
        job_ids = default_queue.get_job_ids()
    elif status == "started":
        job_ids = default_queue.started_job_registry.get_job_ids()
    elif status == "deferred":
        job_ids = default_queue.deferred_job_registry.get_job_ids()
    elif status == "finished":
        job_ids = default_queue.finished_job_registry.get_job_ids()
    elif status == "failed":
        job_ids = default_queue.failed_job_registry.get_job_ids()
    elif status == "all":
        queued_ids = default_queue.get_job_ids()
        started_ids = default_queue.started_job_registry.get_job_ids()
        deferred_ids = default_queue.deferred_job_registry.get_job_ids()
        finished_ids = default_queue.finished_job_registry.get_job_ids()
        failed_ids = default_queue.failed_job_registry.get_job_ids()
        job_ids = queued_ids + started_ids + deferred_ids + finished_ids + failed_ids
    else:
        job_ids = []
    job_attributes = []
    for job_id in job_ids:
        job = Job.fetch(job_id, connection=rq2.connection)
        if job.enqueued_at is not None:
            enqueued_at = (job.enqueued_at + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            enqueued_at = ''
        if job.started_at is not None:
            started_at = (job.started_at + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            started_at = ''
        if job.ended_at is not None:
            ended_at = (job.ended_at + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            ended_at = ''

        job_attributes.append({"job_id": job_id,
                               "args": job.args,
                               "kwargs": job.kwargs,
                               "result": job.result,
                               "enqueued_at": enqueued_at,
                               "started_at": started_at,
                               "ended_at": ended_at,
                               "exc_info": job.exc_info,
                               "origin": job.origin,
                               "job_status": job.get_status(),
                               "ttl": job.get_result_ttl(),
                               })

    # 按时间降序
    job_attributes = sorted(job_attributes, key=lambda k: k['ended_at'], reverse=True)

    # 分页
    total = len(job_ids)
    total_page = math.ceil(total / page_size)
    offset = (page - 1) * page_size

    return response(data=job_attributes[offset:(offset + page_size)], total=total, total_page=total_page)


@api.delete('/<job_id>')
@permission(name='删除异步任务', module=PermissionGroup.JOB, uuid='4e440bab-9c06-11eb-8b14-8cec4baea5d8')
# @role_required
def del_job(path: PathJob):
    """任务删除"""
    job = Job.fetch(path.job_id, connection=rq2.connection)
    if job is not None:
        send_stop_job_command(rq2.connection, path.job_id)
        job.delete()
        return response()
    else:
        raise JobNotExistException()


@api.put('/<job_id>')
@permission(name='重试异步任务', module=PermissionGroup.JOB, uuid='54f0ed18-9c06-11eb-9220-8cec4baea5d8')
@role_required
def retry_job(path: PathJob):
    """重试异步任务"""
    job = Job.fetch(path.job_id, connection=rq2.connection)
    if job is not None:
        try:
            job.requeue()
            return response()
        except InvalidJobOperation:
            raise JobNotRetryException()
    else:
        raise JobNotExistException()