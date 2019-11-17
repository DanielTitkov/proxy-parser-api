import datetime
import sqlalchemy
import requests
import bs4

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine

from typing import Dict, Optional, Any

from config import Config


def form_pg_connection_string(config: Config) -> str:
    return 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        user=config.DBUSER,
        password=config.DBPASSWORD,
        host=config.DBHOST,
        port=config.DBPORT,
        database=config.DBUSER,
    )


Base = declarative_base() # type: Any
config = Config()
engine = create_engine(form_pg_connection_string(config))
Session = scoped_session(sessionmaker(bind=engine))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return "<Post(title='{}'>".format(self.title)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "created": self.created,
        }

    @classmethod
    def fetch_all(cls, config: Config) -> None:
        Session
        response = requests.get(config.TAGRET_URL)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        links = soup.select(config.POST_SELECTOR)
        try:
            Session.add_all(
                (cls(url=l['href'], title=l.contents[0]) for l in links)
            )
            Session.commit()
        except Exception as e:
            Session.rollback()
            print("session failed", e)
            raise
        finally:
            Session.close()

    @classmethod
    def query_posts(cls, sort: str, order: str, limit: str, offset: str) -> Any:
        query = Session.query(Post) \
            .order_by(
                getattr(Post, sort).desc()
                if order == "desc"
                else getattr(Post, sort)
        ) \
            .limit(limit) \
            .offset(offset)
        return query


Base.metadata.create_all(engine)
