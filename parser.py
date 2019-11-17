import requests
import bs4
import sqlalchemy

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
from loguru import logger

from config import Config
from database import Post, Session


if __name__ == "__main__":
    redis_conn = Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
    )
    scheduler = Scheduler(connection=redis_conn)

    # clean old jobs (in case of restart etc)
    for job in scheduler.get_jobs():
        scheduler.cancel(job)

    scheduler.cron(
        Config.PARSER_SCHEDULE_STRING,
        func=Post.fetch_all,
        args=[Config],
        kwargs={},
        repeat=None,  # repeat forever
        queue_name="default",
        meta={}
    )

    logger.info(f"parser job issued with schedule: {Config.PARSER_SCHEDULE_STRING}")
