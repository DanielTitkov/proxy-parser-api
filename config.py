import os
import multiprocessing


class Config:

    # database
    DBUSER = os.getenv("DBUSER", "af")
    DBPASSWORD = os.getenv("DBPASSWORD")
    DBHOST = os.getenv("DBHOST", "localhost")
    DBPORT = os.getenv("DBPORT", 5432)

    # redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT= os.getenv("REDIS_PORT", 6379)
    REDIS_DB= os.getenv("REDIS_DB", 0) 

    # API
    APIPORT = os.getenv("APIPORT", 8000)
    APIWORKERS = os.getenv("APIWORKERS", multiprocessing.cpu_count() * 2 + 1)

    # parser
    TAGRET_URL = "https://news.ycombinator.com/"
    POST_SELECTOR = "a.storylink"

    # query args
    ARGS = {
        "sort": {
            "type": "nominal",
            "values": ["id", "title"],
            "default": "id",
        },
        "order": {
            "type": "nominal",
            "values": ["asc", "desc"],
            "default": "asc",
        },
        "offset": {
            "type": "interval",
            "values": (0, 100),
            "default": 0,
        },
        "limit": {
            "type": "interval",
            "values": (0, 1000),
            "default": 5,
        },
        "update": {
            "type": "nominal",
            "values": ["sync", "async", "none"],
            "default": "none",
        }
    }

    # Parser
    PARSER_SCHEDULE_STRING = "* * * * *"