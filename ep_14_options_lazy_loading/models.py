# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=2fwdjkL0jqw

from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from datetime import datetime

db_url = 'sqlite:///ep_14_options_lazy_load.db'

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    status: Mapped[str | None]
    posts: Mapped[list['Post']] = relationship(
        backref='user',
        lazy='select',
    )
    preference: Mapped['Preference'] = relationship(
        backref='user',
        lazy='joined',
    )

    def __repr__(self):
        return f'<User {self.name} >'

class Preference(Base):
    __tablename__ = 'preferences'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    dark_mode: Mapped[bool] = mapped_column(default=False)
    speed: Mapped[float] = mapped_column(default=1.0)

    def __repr__(self):
        return f'<Preferences {self.id} >'

class Post(Base):
    __tablename__ = 'posts'
    active: Mapped[bool] = mapped_column(default=True)
    date: Mapped[datetime] = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    detail: Mapped['Detail'] = relationship(backref='post', lazy='select')

    def __repr__(self):
        return f'<Post {self.id} >'


class Detail(Base):
    __tablename__ = 'details'
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Detail {self.id} - content: {self.content}>'


# Create the database tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    user_1 = User(name='Zeq', preference=Preference(dark_mode=True, speed=2.5))
    user_1.posts = [
        Post(detail=Detail(content='This is an example post detail')),
        Post(detail=Detail(content='Subscribe to Zeq Tech!'), active=True),
    ]

    user_2 = User(name='Bill', preference=Preference())
    user_2.posts = [
        Post(detail=Detail(content='This is another example of some post details')),
        Post(detail=Detail(content='Yes!')),
    ]

    session.add_all([user_1, user_2])
    session.commit()
