from flask import Flask, jsonify, make_response, request
from rq import Queue
from redis import Redis

from config import Config
from database import Post, Base, init_db_session, form_pg_connection_string
from helpers.url import parse_args, validate_args


app = Flask(__name__)


@app.route('/posts/')
def get_posts():
    config = Config()  # do somewhere else
    session = init_db_session(Base, form_pg_connection_string(config), False)

    args = parse_args(config.ARGS, request.args)
    valid, message = validate_args(config.ARGS, args)
    if not valid:
        return make_response(jsonify({"error": message}), 400)

    if args["update"] == "sync":
        Post.fetch_all(config)
    if args["update"] == "async":
        redis_conn = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB
        )
        q = Queue(connection=redis_conn)  # no args implies the default queue
        job = q.enqueue(Post.fetch_all, config)
        return make_response(jsonify({"message": f"update requested, job id: {job.id}"}), 200)

    query = session.query(Post) \
        .order_by(
            getattr(Post, args["sort"]).desc()
            if args["order"] == "desc"
            else getattr(Post, args["sort"])
    ) \
        .limit(args["limit"]) \
        .offset(args["offset"])

    return make_response(jsonify([p.to_dict() for p in query]), 200)


if __name__ == '__main__':
    app.run()
