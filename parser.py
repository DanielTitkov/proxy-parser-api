import requests
import bs4
import sqlalchemy

from config import Config
from database import Post, Base, init_db_session, form_pg_connection_string

from typing import Optional


def update_posts(config: Config, session: Optional[sqlalchemy.orm.session.Session]=None) -> None:
    if not session:
        session = init_db_session(Base, form_pg_connection_string(config))
    response = requests.get(config.TAGRET_URL)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    links = soup.select(config.POST_SELECTOR)
    session.add_all(
        (Post(url=l['href'], title=l.contents[0]) for l in links)
    )
    session.commit()    
    session.close()


if __name__ == "__main__":
    config = Config()

    session = init_db_session(Base, form_pg_connection_string(config))

    update_posts(config, session)
