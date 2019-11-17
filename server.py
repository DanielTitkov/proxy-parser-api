from flask import Flask, jsonify, make_response, request
from rq import Queue
from redis import Redis
from loguru import logger

from config import Config
from database import Post, Base, Session, form_pg_connection_string
from helpers.url import parse_args, validate_args

from typing import Any


app = Flask(__name__)


@app.route('/posts/')
def get_posts() -> Any:
    args = parse_args(Config.ARGS, request.args)
    valid, message = validate_args(Config.ARGS, args)
    if not valid:
        return make_response(jsonify({"error": message}), 400)

    if args["update"] == "sync":
        logger.info("sync update requested")
        Post.fetch_all(Config)
        logger.info("sync update done")
    if args["update"] == "async":
        logger.info("async update requested")
        redis_conn = Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB
        )
        q = Queue(connection=redis_conn)  # no args implies the default queue
        job = q.enqueue(Post.fetch_all, Config)
        logger.info(f"job for async update issued, job id: {job.id}")
        return make_response(jsonify({"message": f"update requested, job id: {job.id}"}), 200)

    query = Post.query_posts(
        sort=args["sort"],
        order=args["order"],
        limit=args["limit"],
        offset=args["offset"],
    )

    return make_response(jsonify([p.to_dict() for p in query]), 200)


if __name__ == '__main__':
    app.run()
