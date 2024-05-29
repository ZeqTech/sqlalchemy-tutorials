# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================

from typing import Optional

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine('sqlite:///ep_10_relationships.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]

    # One to Many relationship with Annotation
    posts: Mapped[list['Post']] = relationship()


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # One to One relationship with Annotation
    content: Mapped['Content'] = relationship()


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    data: Mapped[str]


# Create the database tables
Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    user = User(
        name='Zeq Tech', posts=[Post(content=Content(data='This is some content'))]
    )
    session.add(user)
    session.commit()

user = session.scalar(select(User))
print(f'\nUser {user.id}: {user.name} - {user.posts[0].content.data} \n')

user = session.query(User).first()
print(f'\nUser {user.id}: {user.name} - {user.posts[0].content.data} \n')
