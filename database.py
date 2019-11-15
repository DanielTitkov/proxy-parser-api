import datetime
import sqlalchemy
import requests
import bs4

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine

from typing import Dict, Optional

from config import Config


def form_pg_connection_string(config: Config) -> str:
    return 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        user=config.DBUSER,
        password=config.DBPASSWORD,
        host=config.DBHOST,
        port=config.DBPORT,
        database=config.DBUSER,
    )


def init_db_session(
    base: sqlalchemy.ext.declarative.DeclarativeMeta,
    connection_string: str,
    create_tables: bool = True,
) -> sqlalchemy.orm.Session:
    engine = create_engine(connection_string)
    if create_tables:
        base.metadata.create_all(engine)
    return sqlalchemy.orm.sessionmaker(bind=engine)()


Base = declarative_base()


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
    def fetch_all(cls, config: Config, session: Optional[sqlalchemy.orm.session.Session] = None) -> None:
        if not session:
            session = init_db_session(Base, form_pg_connection_string(config))
        response = requests.get(config.TAGRET_URL)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        links = soup.select(config.POST_SELECTOR)
        session.add_all(
            (cls(url=l['href'], title=l.contents[0]) for l in links)
        )
        session.commit()
        session.close()
