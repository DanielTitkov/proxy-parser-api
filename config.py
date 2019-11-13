import os


class Config:

    # database
    DBUSER = os.getenv("DBUSER", "af")
    DBPASSWORD = os.getenv("DBPASSWORD", "af")
    DBHOST = os.getenv("DBHOST", "localhost")
    DBPORT = os.getenv("DBPORT", 5432)

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
