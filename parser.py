import requests
import bs4
import sqlalchemy

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

from config import Config
from database import Post, Session


if __name__ == "__main__":
    config = Config()

    redis_conn = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
    )
    scheduler = Scheduler(connection=redis_conn)

    # clean old jobs (in case of restart etc)
    for job in scheduler.get_jobs():
        scheduler.cancel(job)

    scheduler.cron(
        config.PARSER_SCHEDULE_STRING,
        func=Post.fetch_all,
        args=[config],
        kwargs={},
        repeat=None,  # repeat forever
        queue_name="default",
        meta={}
    )
