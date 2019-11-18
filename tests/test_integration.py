import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(currentdir))

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import time
import requests
import pytest

from config import Config
from database import Base, Session, engine, form_pg_connection_string, Post


URL = os.getenv("TESTURL", "http://localhost:8000/posts")


def recreate_db():
    engine.execute(
        """SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'test'
        AND pid <> pg_backend_pid();"""
    )  # this is needed because other sessions are in different containers
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
    time.sleep(0.1)


@pytest.fixture(scope="function")
def db_session():
    recreate_db()
    yield Session()
    # Session.close_all()
    recreate_db()


def test_empty(db_session):
    r = requests.get(URL)
    assert r.json() == []


def test_async_update(db_session):
    r = requests.get(
        URL,
        params={
            "update": "async",
        }
    )
    time.sleep(2)
    r = requests.get(
        URL,
        params={
            "limit": 1000,
        }
    )
    assert len(r.json()) == 30


def test_sync_update(db_session):
    r = requests.get(
        URL,
        params={
            "update": "sync",
            "limit": 1000,
        }
    )
    assert len(r.json()) == 30


def test_query_params(db_session):
    expected = [
        {
            "id": 5,
            "title": "The Efficiency-Destroying Magic of Tidying Up",
            "url": "https://florentcrivello.com/index.php/2019/09/04/the-efficiency-destroying-magic-of-tidying-up/"
        },
        {
            "id": 12,
            "title": "Tetrachromats: people who see colors invisible to most of us",
            "url": "https://www.bbc.com/future/article/20140905-the-women-with-super-human-vision"
        },
        {
            "id": 23,
            "title": "Staying Focused on Projects",
            "url": "https://www.brendonbody.com/2019/11/18/staying-focused/"
        }
    ]
    r = requests.get(
        URL,
        params={
            "update": "sync",
            "limit": 3,
            "offset": 5,
            "sort": "title",
            "order": "desc",
        }
    )
    assert len(r.json()) == 3 and all(
        [p[0][k]==p[1][k] for p in zip(expected, r.json()) for k in ['title', "id", "url"]]
    )


def test_bad_limit_value():
    expected = {
        "error": "Wrong value '2000' for argument 'limit'. Suppported values are: (0, 1000)"
    }
    r = requests.get(
        URL,
        params={
            "limit": 2000,
        }
    )
    assert r.json() == expected