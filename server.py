from flask import Flask, jsonify, make_response, request
from rq import Queue
from redis import Redis

from config import Config
from database import Post, Base, init_db_session, form_pg_connection_string
from parser import update_posts
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
        update_posts(config)
    if args["update"] == "async":
        redis_conn = Redis()
        q = Queue(connection=redis_conn)  # no args implies the default queue
        job = q.enqueue(update_posts, config)
        print(len(q))
        return make_response(jsonify({"message": "update has been requested"}), 200)

    query = session.query(Post) \
        .order_by(
            getattr(Post, args["sort"]).desc() 
            if args["order"] == "desc" 
            else getattr(Post, args["sort"])
        ) \
        .limit(args["limit"]) \
        .offset(args["offset"])

    posts = [p.to_dict() for p in query]

    return make_response(jsonify(posts), 200)


if __name__ == '__main__':
    app.run()
