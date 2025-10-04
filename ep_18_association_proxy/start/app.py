# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=jmjuaSVRWPY

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, User, Article

engine = create_engine('sqlite:///:memory:', echo=False)
Base.metadata.create_all(engine)

with Session(engine) as session:
    zeq = User(name='Zeq Tech')
    mark = User(name='Mark')
    art1 = Article(title='Intro to SQLAlchemy')
    art2 = Article(title='Advanced Python Tips')

    zeq.articles.extend([art1, art2])
    mark.articles.append(art1)

    session.add_all([zeq, mark])
    session.commit()

    # Print article titles for each user
    print([article.title for article in zeq.articles])
    print([article.title for article in mark.articles])

    # Print user names for each article
    print([user.name for user in art1.users])
    print([user.name for user in art2.users])
