import datetime
import requests
import bs4

from loguru import logger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine

from typing import Dict, Optional, Any, Union, Type

from config import Config


def form_pg_connection_string(config: Config) -> str:
    return 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        user=config.DBUSER,
        password=config.DBPASSWORD,
        host=config.DBHOST,
        port=config.DBPORT,
        database=config.DBUSER,
    )

Base = declarative_base()  # type: Any
engine = create_engine(form_pg_connection_string(Config))
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
    def fetch_all(cls, config: Union[Config, Type[Config]], only_new: bool = True) -> None:
        response = requests.get(config.TAGRET_URL)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        links = soup.select(config.POST_SELECTOR)
        posts = [cls(url=l['href'], title=l.contents[0]) for l in links]
        logger.info(f"extracted {len(posts)} posts")
        if only_new:
            try: 
                new_titles = [p.title for p in posts]
                existing_posts = {
                    p[0] for p in Session.query(Post.title).filter(Post.title.in_(new_titles)).all()
                }
                logger.info(f"already in database: {existing_posts}")
                posts = [p for p in posts if p.title not in existing_posts]
            except Exception as e:
                Session.rollback()
                logger.error(f"database operation failed: {e}")
            finally:
                Session.close()            
        try:
            Session.add_all(posts)
            Session.commit()
            logger.info(f"saved posts to database: {posts}")
        except Exception as e:
            Session.rollback()
            logger.error(f"database operation failed: {e}")
            raise
        finally:
            Session.close()

    @classmethod
    def query_posts(cls, sort: str, order: str, limit: str, offset: str) -> Any:
        try: 
            query = Session.query(Post) \
                .order_by(
                    getattr(Post, sort).desc()
                    if order == "desc"
                    else getattr(Post, sort)
            ) \
                .limit(limit) \
                .offset(offset)
        except Exception as e:
            Session.rollback()
            logger.error(f"database operation failed: {e}")
            raise
        finally:
            Session.close()
        return query


Base.metadata.create_all(engine)
