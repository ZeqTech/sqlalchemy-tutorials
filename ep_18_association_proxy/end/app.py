# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=jmjuaSVRWPY

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, User, Article

engine = create_engine('sqlite://', echo=False)
Base.metadata.create_all(engine)

with Session(engine) as session:
    zeq = User(name='Zeq Tech')
    mark = User(name='Mark')
    art1 = Article(title='Intro to SQLAlchemy')
    art2 = Article(title='Advanced Python Tips')

    zeq.articles.extend([art1, art2])
    mark.articles.append(art1)

    session.add_all([zeq, mark, art1, art2])
    session.commit()

    # Print article titles for each user
    print(zeq.article_titles)  # ['Intro to SQLAlchemy', 'Advanced Python Tips']
    print(mark.article_titles)  # ['Intro to SQLAlchemy']

    # Print user names for each article
    print(art1.users_name)  # ['Zeq Tech', 'Mark']
    print(art2.users_name)  # ['Zeq Tech']
